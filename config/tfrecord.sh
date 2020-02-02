# Parameters passed to bert/create_pretraining_data.py.

CREATE_TFRECORD_PARAMS="
--vocab_file=$WORDPIECE_VOCAB_PATH
--do_lower_case=false
--do_whole_word_mask=true
--dupe_factor=10
"
CREATE_TFRECORD_PARAMS_128="
--max_seq_length=128
--max_predictions_per_seq=20
"
CREATE_TFRECORD_PARAMS_512="
--max_seq_length=512
--max_predictions_per_seq=77
"

