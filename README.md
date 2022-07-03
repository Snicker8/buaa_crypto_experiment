# BUAA Crypto Experiment

Codes and reports for BUAA Cryptography Experiment in 2022 Spring.

## Directions

- Most programs are written in Python, other programs are written in C due to efficiency issues.
- Due to the introduction of OJ Platform from 2022 Spring, the code has input and output requirements, and the course is more standardized.
- On the names of dictionaries and files
  - **ex#** stands for experiment #
  - **c#** stands for question # of the experiment, and it is compulsory
  - **op#** stands for question # of the experiment, and it is optional
  - **s#** stands for step # of a problem
- Learning and improving are encouraged, but **DO NOT COPY COMPLETELY !**

## Codes

File name clearly shows what file contains.

Followings are directions of some special files.

- ex2/op10
  - [ex2/op10](codes/ex2_classical_cipher/op10_frequency_attack_2.py) - only prints the result
  - [op10/s1](codes/ex2_classical_cipher/op10_related/s1_generate_plaintext_subversion.py) & [op10/s2](codes/ex2_classical_cipher/op10_related/s2_generate_plaintext.py) - shows the derivation step
  - [op10/s3](codes/ex2_classical_cipher/op10_related/s3_split_plaintext.py) - to split text by words (required [wordninja](https://github.com/keredson/wordninja))
  - more information can be found in [report](reports/ex2_classical_cipher.pdf).


- ex3/des
  - [des_v1](codes/ex3_data_encryption_standard_(des)/c1_des_v1.py) - original version without optimization
  - [des_v2](codes/ex3_data_encryption_standard_(des)/c1_des_v2.py) - optimized version by Python (actually it didn't work)
  - [des_v3](codes/ex3_data_encryption_standard_(des)/op4_des_v3.cpp) - optimized version by C++ (just rewrite in C++)
  - [des_v4](codes/ex3_data_encryption_standard_(des)/op4_des_v4.c) - optimized version by C (SPbox optimization)
- ex3/op3

  - [ex3/op3](codes/ex3_data_encryption_standard_(des)/op3_weak_&_semi_weak_key.py) - only prints the result
  - [op3/s1](codes/ex3_data_encryption_standard_(des)/op3_related/s1_generate_weak_key.py) & [op3/s2](codes/ex3_data_encryption_standard_(des)/op3_related/s2_ganerate_semi_weak_key.py) - shows the derivation step
  - more information can be found in [report](reports/ex3_data_encryption_standard_(des).pdf).
- ex5

  - [ex5/related](codes/ex5_sm4_&_work_mode/ex5_related) - to answer the thinking questions
  - [figures](codes/ex5_sm4_&_work_mode/ex5_related/figures/) includes encrypted figures by the work mode of [cbc](codes/ex5_sm4_&_work_mode/ex5_related/cbc_encrypt.py) & [ecb](codes/ex5_sm4_&_work_mode/ex5_related/ecb_encrypt.py)
  - [time_record](codes/ex5_sm4_&_work_mode/ex5_related/time_record.py) - record times in sm4
  - [print_2_excel](codes/ex5_sm4_&_work_mode/ex5_related/print_2_excel.py) - print record to [excel](codes/ex5_sm4_&_work_mode/ex5_related/time_record.xls)
  - more information can be found in [report](reports/ex5_sm4_&_work_mode.pdf).
- ex9/op5
  - [ex9/op5](codes/ex9_hash_function/op5_(sha1)_birthday_attack_ii.py) - only prints the result
  - [op5/s1](codes/ex9_hash_function/op5_related/s1_generate_deformed_message.py) & [op5/s2](codes/ex9_hash_function/op5_related/s2_find_pairs.py) - generate pairs
  - more information can be found in [report](reports/ex9_hash_function.pdf).
- callgraph - generate function call graph, see the [program](codes/callgraph.py) for usage examples.

## Reports

- Reports for each experiment.
- Composed by Microsoft Office (Word & PowerPoint, with AxMath plugin).
- Simplified Chinese only.

## Thanks

- Thanks to the guidance from teachers and assistants in *Mathematical Fundamentals of Information Security*.
- Thanks to the guidance from teachers and assistants in *Cryptography* and *Cryptography Experiments*.
- Thanks to the sharings from [Zheng Yaowei](https://github.com/hiyouga/cryptography-experiment), [Fu Yunhao](https://github.com/FYHSSGSS/BUAA-CryptoLab), [Huang Xiang](https://github.com/xiangsam/Cryptography_Experiment).
- Thanks to the help of [Cui Shibo](https://github.com/JadeiteMind).
