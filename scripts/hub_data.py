"""Push the built data (or the teacher logits) to a private Hugging Face dataset repo, or pull a pushed
revision back (vilatent.hub). Needs HF_TOKEN in the environment: write access to push, read access to pull.

  push  uploads every file of the bundle and MANIFEST_<bundle>.json in one commit; prints the commit
        (revision) and writes it to data/hub_<bundle>_revision.txt. Hand that revision to the project owner.
  pull  downloads the bundle at --revision into the repository, then checks every file against the
        manifest; refuses to start if a local file of the bundle already exists with other content.

Usage:
  python scripts/hub_data.py push --bundle data --repo thanthienhai/vilatent-data
  python scripts/hub_data.py pull --bundle data --repo thanthienhai/vilatent-data --revision <commit>
  python scripts/hub_data.py push --bundle data --repo thanthienhai/vilatent-data --dry-run   # list only
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

from vilatent.hub import BUNDLES, build_manifest, check_files, conflicts, manifest_name, write_manifest


def push(args) -> None:
    manifest = build_manifest(".", args.bundle)
    total = sum(f["size"] for f in manifest["files"].values())
    print(f"{args.bundle}: {len(manifest['files'])} files, {total / 2**30:.2f} GiB, built at {manifest['git_commit']}")
    if manifest["git_commit"].endswith("-dirty") or manifest["git_commit"] == "unknown":
        print("WARNING: the working tree is not a clean commit; the manifest records it as is")
    if args.dry_run:
        for path, info in manifest["files"].items():
            print(f"  {path}  {info['size']:>12}  {info['sha256'][:12]}")
        return
    from huggingface_hub import CommitOperationAdd, HfApi

    api = HfApi()
    api.create_repo(args.repo, repo_type="dataset", private=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        mpath = Path(tmp) / manifest_name(args.bundle)
        write_manifest(mpath, manifest)
        ops = [CommitOperationAdd(path_in_repo=p, path_or_fileobj=p) for p in manifest["files"]]
        ops.append(CommitOperationAdd(path_in_repo=manifest_name(args.bundle), path_or_fileobj=str(mpath)))
        info = api.create_commit(args.repo, ops, repo_type="dataset",
                                 commit_message=f"{args.bundle} built at {manifest['git_commit']}")
    revision = info.oid
    Path(f"data/hub_{args.bundle}_revision.txt").write_text(revision + "\n", encoding="utf-8")
    print(json.dumps({"repo": args.repo, "bundle": args.bundle, "revision": revision}))


def pull(args) -> None:
    from huggingface_hub import hf_hub_download, snapshot_download

    mfile = hf_hub_download(args.repo, manifest_name(args.bundle), repo_type="dataset", revision=args.revision)
    manifest = json.loads(Path(mfile).read_text(encoding="utf-8"))
    clash = conflicts(".", manifest)
    if clash:
        sys.exit(f"local files differ from {args.repo}@{args.revision}, not replacing them: {clash[:5]} "
                 f"({len(clash)} files); move them away first")
    missing = check_files(".", manifest)
    if missing:
        snapshot_download(args.repo, repo_type="dataset", revision=args.revision, local_dir=".",
                          allow_patterns=missing)
    bad = check_files(".", manifest)
    if bad:
        sys.exit(f"{len(bad)} files do not match the manifest after the download, e.g. {bad[:3]}")
    print(json.dumps({"repo": args.repo, "bundle": args.bundle, "revision": args.revision,
                      "files": len(manifest["files"]), "built_at": manifest["git_commit"], "verified": True}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["push", "pull"])
    ap.add_argument("--bundle", choices=list(BUNDLES), required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--revision", help="commit to pull (required for pull: a branch name could move)")
    ap.add_argument("--dry-run", action="store_true", help="push: list the files and stop")
    args = ap.parse_args()
    if args.action == "pull" and not args.revision:
        ap.error("pull needs --revision (the commit printed by push)")
    push(args) if args.action == "push" else pull(args)


if __name__ == "__main__":
    main()
