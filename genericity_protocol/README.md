# Protocol code and design for genericity annotation

This folder contains the styling and markup files for running the genericity protocol on Amazon Mechanical Turk. It also contains the code necessary to generate the .csv datafile that MTurk requires as input. To generate these datafiles, ensure that the scripts point to the current location of the [Universal Dependencies v1.2 dataset](https://github.com/UniversalDependencies/UD_English-EWT/releases/tag/r1.2). You are free to use the scripts and the markup files to rerun the protocol as is, or to generate your own protocol. For a detailed description of the protocol and data collected please refer to the following papers. If you use these scripts or protocol designs  in a presentation or publication, we ask that you cite the following paper.

# Archive of genericity data

This archive contains data from the experiments described in Section 4 of the following paper.

V. S. Govindarajan, B. Van Durme. 2016, & White, A. S. [Decomposing Generalization: Models of Generic, Habitual, and Episodic Statements](). In *Arxiv*.

If you make use of this data set in a presentation or publication, we ask that you please cite this paper.

There are four files: `arg_long_data.tsv`, `arg_norm_data.tsv`, `pred_long_data.tsv`, and `pred_norm_data.tsv`. The first two contain annotations for arguments in sentences from the [Universal Dependencies v1.2 dataset](https://github.com/UniversalDependencies/UD_English-EWT/releases/tag/r1.2), and the latter two contain annotations for predicates. The `long` datasets contain raw annotations with the annotation confidence measures, while the `norm` datasets contain the data after normalisation(which is described in the paper.)

The column descriptions and values for `arg_long_data.tsv` can be found below.

| Column            | Description       | Values            |
|-------------------|-------------------|-------------------|
| Split | The dataset split to which annotation belongs | `train`, `dev`, `test` |
| Annotator.ID | The annotator that provided the response | `0`,.....,`100` |
| Sentence.ID | The file and sentence number of the sentence in the English Universal Dependencies v1.2 treebank with the format `LANGUAGE-CORPUS-SPLIT.ANNOTATION SENTNUM` |  |
| Arg.Token | The root argument index in the sentence(from [PredPatt]()) | `0`,.....,`100` |
| Arg.Span | The indices of all tokens in the argument | ``0,1,2`, `3,4`` |
| Pred.Token | The index of the root of the governing predicate | `0`,.....,`100` |
| Pred.Span | The indices of all tokens in the governing predicate | ``0,1,2`, `3,4`` |
| Arg.Word | The argument token | `string` |
| Arg.Lemma | The argument lemma | `string` |
| Is.Particular | The particular property annotation | `True, False` |
| Is.Particular.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |
| Is.Kind | The kind property annotation | `True, False` |
| Is.Kind.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |
| Is.Abstract | The abstract property annotation | `True, False` |
| Is.Abstract.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |


The column descriptions and values for `arg_norm_data.tsv` can be found below.

| Column            | Description       | Values            |
|-------------------|-------------------|-------------------|
| Split | The dataset split to which annotation belongs | `train`, `dev`, `test` |
| Annotator.ID | The annotator that provided the response | `0`,.....,`100` |
| Sentence.ID | The file and sentence number of the sentence in the English Universal Dependencies v1.2 treebank with the format `LANGUAGE-CORPUS-SPLIT.ANNOTATION SENTNUM` |  |
| Arg.Token | The root argument index in the sentence(from [PredPatt]()) | `0`,.....,`100` |
| Arg.Span | The indices of all tokens in the argument | ``0,1,2`, `3,4`` |
| Is.Particular.Norm | The normalised particular score | `[-inf, inf]` |
| Is.Kind.Norm | The normalised kind score | `[-inf, inf]` |
| Is.Abstract.Norm | The normalised abstract score | `[-inf, inf]` |

The column descriptions and values for `pred_long_data.tsv` can be found below.

| Column            | Description       | Values            |
|-------------------|-------------------|-------------------|
| Split | The dataset split to which annotation belongs | `train`, `dev`, `test` |
| Annotator.ID | The annotator that provided the response | `0`,.....,`100` |
| Sentence.ID | The file and sentence number of the sentence in the English Universal Dependencies v1.2 treebank with the format `LANGUAGE-CORPUS-SPLIT.ANNOTATION SENTNUM` |  |
| Pred.Token | The index of the root of the governing predicate | `0`,.....,`100` |
| Ann.Token | The index of the tokens highlighted to annotators(subset of Pred.Span) | `0`,.....,`100` |
| Pred.Span | The indices of all tokens in the governing predicate | ``0,1,2`, `3,4`` |
| Arg.Token | The index of the root dependent argument | `0`,.....,`100` |
| Arg.Span | The indices of all tokens in the dependent arguments | ``0,1,2;7,8`, `3,4`` |
| Pred.Word | The predicate token | `string` |
| Pred.Lemma | The predicate lemma | `string` |
| Is.Particular | The particular property annotation | `True, False` |
| Is.Particular.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |
| Is.Dynamic | The dynamic property annotation | `True, False` |
| Is.Dynamic.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |
| Is.Hypothetical | The hypothetical property annotation | `True, False` |
| Is.Hypothetical.Confidence | The 5-point Likert scale annotation confidence of the property | `0, 1, 2, 3, 4` |

The column descriptions and values for `pred_norm_data.tsv` can be found below.

| Column            | Description       | Values            |
|-------------------|-------------------|-------------------|
| Split | The dataset split to which annotation belongs | `train`, `dev`, `test` |
| Annotator.ID | The annotator that provided the response | `0`,.....,`100` |
| Sentence.ID | The file and sentence number of the sentence in the English Universal Dependencies v1.2 treebank with the format `LANGUAGE-CORPUS-SPLIT.ANNOTATION SENTNUM` |  |
| Pred.Token | The index of the root of the governing predicate | `0`,.....,`100` |
| Pred.Span | The indices of all tokens in the governing predicate | ``0,1,2`, `3,4`` |
| Is.Particular.Norm | The normalised particular score | `[-inf, inf]` |
| Is.Dynamic.Norm | The normalised dynamic score | `[-inf, inf]` |
| Is.Hypothetical.Norm | The normalised hypothetical score | `[-inf, inf]` |
