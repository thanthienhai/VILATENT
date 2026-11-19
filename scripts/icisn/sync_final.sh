#!/usr/bin/env bash
cd /c/Users/PC/Coding/thienthan/THS/VILATENT
for pair in "results/icisn_xquad/single:results/icisn/xquad/single" "results/icisn_xquad/long:results/icisn/xquad/long" \
            "results/icisn_test/single:results/icisn/test_extra/single" "results/icisn_test/long_s1:results/icisn/test_extra/long"; do
  src=${pair%%:*}; dst=${pair##*:}; mkdir -p $dst
  for s in $(ssh gpu1080 "cd ~/vilatent_mlqa/$src 2>/dev/null && ls *.summary.json 2>/dev/null"); do
    stem=${s%.summary.json}
    [ -f $dst/$stem.jsonl ] && [ -f $dst/$s ] && continue
    scp -q gpu1080:vilatent_mlqa/$src/$stem.jsonl gpu1080:vilatent_mlqa/$src/$s $dst/
  done
done
python -X utf8 scripts/icisn/judge_new.py primary 16 >> results/icisn/judge/judge_new_primary.log 2>&1
python -X utf8 scripts/icisn/judge_new.py secondary 12 --only-hyp >> results/icisn/judge/judge_new_secondary.log 2>&1
echo SYNC_FINAL_DONE >> results/icisn/judge/judge_new_primary.log
