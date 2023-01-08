# What NLPytaly is and what it does

​	NLPytaly is a research project in Computational Linguistics and Natural Language Understanding started in 2019 by Ignazio Mauro Mirto (associate professor of General Linguistics at the University of Palermo, Italy). The software is mainly designed to obtain machine-readable meaning and **entailments** from Italian sentences. Given the limited number of supported constructions (described below), the tool is currently more effective when dealing with simple, monopredicative sentences (e.g. *Max spera* (Max hopes)), but also with a number of multipredicative sentences (e.g. the so-called light verb constructions, e.g. *Max nutre una speranza* (Max has/harbors a hope)).

​	The tool functions by means of a rule-based system implemented with Python 3.10. Basic operations are performed with TreeTagger, a statistical parser which only provides: a) words as they occur in the text, b) their POS, and c) their lemmas. NLPytaly permits the modification, where necessary, of such outcomes, whether that be the POS or the lemma (errors occur in both), and returns a richer morphosyntactic representation, which provides the features number, person, and gender of relevant words, as well as key elements of constituency and negation. Having inputted unannotated text, the following will be obtained:

* an identification of inflected verb phrases and proclitics (if any); 

* an identification of the diathesis on a morphological basis (i.e. without lists of verbs, unless they are necessary). The four diathesis types are: Passive (*Fu applaudito* 'He was applauded'), Middle reflexive (*Mi applaudii* 'I applauded myself'), Middle non-reflexive (*Tornammo* 'We came back'), and, by exclusion, Active (*Noi applaudimmo* 'We applauded'); 

* the detection of most proper names and of noun phrases of three types: a) those introduced by a determiner (e.g. *il gatto* 'the cat'), b) bare plurals (e.g. *Lui ha visto gatti* 'He saw cats'), and c) kinship with zero-article (e.g. *mia moglie* 'my wife'); 

* the explicit identifying of Subject, Direct object, and Indirect object (detection is based on word order; Indirect objects are work in progress); 

* the disambiguation of some function words (e.g. the use of *del*, *della*, *degli* etc as either prepositions or partitive articles; in the latter case, the POS is `DET:part`); 

* the automatic extraction of semantic roles.

​	The outcomes of the tool are available on a website, which can be accessed once a free account has been opened (see below). The following screenshots provide an example with the sentence *Il pubblico applaudì il cantante* (henceforth, sentence (1), The audience applauded the singer):

![image-20210807092744352](README.assets/000.png)

![image-20210807092800518](README.assets/001.png)

## The logic of semantic roles in NLPytaly

​	The meaning which NLPytaly extracts is based on a novel type of semantic role (references are provided below), labeled as **Cognate Semantic Role** (henceforth, CSR). An example will help explain the use of the word ‘cognate’, which researchers employ most in diachronic linguistics (e.g. Latin MǓSCA and Italian *mosca* are etymologically related, and therefore they are **cognate words**): the sentence above, i.e. *Il pubblico applaudì' il cantante* (The audience applauded the singer), is semantically rendered in two steps:

* First step: *applaudì* is identified as the only predicate licensing arguments; it is transitive and therefore the following two CSRs will be assigned:

​			a)   *Chi applaude* (The one who applauds)

​			b)   *Chi è applaudito* (The one who is applauded)

​	In parallel with Case Grammar roles, CSRs depend on predicate-argument relations. However, whilst Case Grammar roles are expressed as one-word labels (e.g. Patient, Experiencer), CSRs are **statements** (more precisely, a specific type of relative clause) which obtain *automatically*. Such roles, which always employ a verb, are called ‘cognate’ because the content morpheme of the verb they contain is that of the predicate licensing arguments. However, suppletive forms may be necessary, mostly when the predicate licensing arguments is **non-verbal** (see below). Therefore, since in a) and b) above the predicate licensing arguments is *applaudì* (she applauded), the CSRs will contain a form of the verb *applaudire* (to applaud/clap).

* Second step: each CSR in a) and b) above will be matched with one of the participants (i.e. referents) which the sentence expresses. With (1) above, this yields the following **pairings**:

​			c)   *Il pubblico è chi applaude* (The audience is the one who applauds)

​			d)   *Il cantante è chi è applaudito* (The singer is the one who is applauded)

​	In order to obtain the outcome in c) and d) above **four fields** have to be identified. The first two, F1 and F2, derive from the predicate-argument structure of the sentence under scrutiny:

​			**F1** – Assignee: Argument/Participant

​			**F2** – Assigner: Predicate

​	For example, in the CSR in c) above, F1 is ‘il pubblico’ and F2 is the verb ‘applaudire’.

​	The third field – **F3** – relates to the morphology of the verb which a CSR must contain. This verb is invariably in the simple present and in the 3rd person. However, it can take three possible forms (others will be necessary): Root (simple present and 3rd person), Root_be+PP (the verb *essere*/*be* occurs, followed by a past participle, as in passives), and Root_si (*si* being a 3rd person clitic). The following screenshot of the sentence *Luigi ha consegnato la relazione a Maria* (Luigi handed the report to Maria) permits to illustrate the three verbal forms in F3:

![image-20210807093021599](README.assets/002.png)

​	The fourth field – **F4** – provides syntactic information on the **origin of the semantic role**, i.e. on the predicate licensing arguments (henceforth, the licenser). The supported constructions from which CSRs derive are of two types: verbal and non-verbal. F4 shows whether the licenser is verbal or non-verbal and, in the latter case, which type of non-verbal predicate assigns semantic roles.

​	So far, **seven types** **of constructions** have been included, which are illustrated below (notice that, with certain constructions, some diatheses are not yet supported):

### Verbal

* ​	OrdinarySemRole (for verbs licensing subjects and direct objects); 

* ​	OrdinaryDativeSemRole (for verbs licensing indirect objects); 

* ​	CausativeSemRole (for the subject licensed by the causative predicates *fare* and *lasciare*); 

### Non-Verbal

* ​	SuppSemRole (for arguments licensed by the nominal predicate of a support verb construction, see screenshot below); this construction involves thousands of nouns; so far, the dictionary includes about 850 of such nouns, which show the potential of the model; 

* ​	JobSemRole (for the subject licensed by the predicative noun of the Job_Fare_Construction, e.g. *Sua moglie fa l'ingegnere* (His wife is an engineer)); the dictionary includes about 4,800 nouns designating jobs; 

* ​	**Ate**SemRole (e.g. *prendere a cannon**ate***; for arguments licensed by a predicative prepositional phrase in a construction in which the verb *prendere* combines with a plural noun ending with the plural suffix -*ate* (about 115 prepositional phrases): *La nave ha preso a cannonate la città* (The ship cannonaded/shelled the town)); overall, there are 145 nouns entering the construction: this dictionary is practically exhaustive; 

* ​	MetterePrepSemRole (for arguments licensed by predicative prepositional phrases in a non-locative construction with the inchoative verb *mettere*, e.g. *La polizia ha messo sotto sorveglianza i locali* (Police put the premises under surveillance)); there are more than 300 non-locative prepositional phrases which enter the construction; so far the dictionary includes about 120.

​	Finally, NLPytaly displays a column, the rightmost, providing an **equative sentence** - exemplified by the pairings in c) and d) above - which provides a semantic representation (more precisely, the propositional content or kernel) of the parsed sentence by describing **who-does-what-to-whom** (as in a theatrical performance), i.e. the role (or involvement) which each participant (beings or things) plays in the scenario the parsed sentence calls forth.

## A distinct, non-traditional, use of 'Entailment'

Regarding paraphrases, i.e. *mutual* entailments, let us consider the relationship between sentences with ordinary verbs such as (2) below, and sentences with support verbs, e.g. (3):

(2)  Sara smiled at Tom

(3)  Sara flashed a smile at Tom

Formally, no **mutual** entailment exists between (2) and (3). This is so because in (2) Sara might have smiled *repeatedly* at Tom, whilst (3) reports a single smile. Thus, there is at least a context in which (2) is true and (3) is false, which rules out a reciprocal entailment and therefore a paraphrase. Only a one-way entailment is found between (2) and (3), since the truth of the latter guarantees the truth of the former.

However, it is intuitively clear that the above one-way entailment does not fully render the semantic interconnections between (2) and (3), which are sentences that share their content morphemes. In both, Sara smiles and both say that Tom is smiled at. From this viewpoint, the semantic relationship is symmetrical and thus reciprocal. How can such a symmetry be captured formally? Put differently, which units of meaning remain constant in (2) and (3)? Cognate semantic roles are appropriate for this task and do the job. A sentence will be reduced to its propositional content: it will be semantically described by using the same number of semantic roles as those assigned by its predicate(s). Thus, the meaning of sentence (2) will be described by means of the following CSRs, because *to smile* is a two-place predicate (intransitive):

<p style="text-align: center">Sara is >she who smiles<</p>
<p style="text-align: center">Tom is >he who is smiled at<</p>

Importantly, also sentence (3) will be described with the above CSRs, because in (3) *to flash* functions as a support verb, thus semantically inert, and the noun *smile*, also working as a two-place intransitive predicate, is the only predicate licensing semantic roles. With sentences such as (2) and (3), CSRs **just intercept the syntactic level where semantic roles are assigned** (by predicative content morphemes) and retrieve the propositional content. The remaining structural levels, destined only to the syntactic closure (realized by means of function morphemes), are ignored. For instance, with CSRs the difference in meaning between e.g. *The policeman arrest**ed** the thief* and *The policeman **will** arrest the thief* is simply ignored (this tense difference is obviously important and can be captured, but is irrelevant if we limit the analysis to the propositional content).

Still concerning the pair *Sara smiled at Tom* and *Sara flashed a smile at Tom*, notice that it is the indefinite article (i.e. a quantifier) within the phrase *a smile* that blocks the reciprocal entailment and thus the paraphrase. CSRs are able to “skip” the effect of quantifiers such as articles and other determiners, e.g. *each* in the following well-known pair (a well-studied active-passive relationship): *Each boy loves a girl* vs *A girl is loved by each boy*, in which once again the determiner *each* blocks the mutual entailment.

## Entailment detection

​	The syntax-semantics interface described above easily allows the identification of a number of entailments. Accordingly, paraphrases between sentences sharing some content morphemes can be identified. For example, a support verb counterpart of *Il pubblico applaudì il cantante* (i.e. sentence (1)) is the following: *Il pubblico fece un applauso al cantante* (The audience gave the singer a round of applause). The tool identifies the construction type, i.e. it identifies the post-verbal *un applauso* as the predicate giving origin to semantic roles (below, see the column Origin of Semantic Role), and it therefore returns the following representations (the first displays the analysis, the second shows the entailment):

![image-20210807093427339](README.assets/003.png)

![image-20210807093457455](README.assets/004.png)

​	Entailment detection is computed on the basis of the sets of cognate semantic roles produced by each sentence. Let *A* be the set of CSRs obtained by the first sentence and *B* the set of CSRs obtained by the second sentence. Then, the following four cases are possible: 

1. if A is a subset of B and *vice versa*, then the tool returns **Mutual entailment** (the **entail each other** in the screenshot above);
2. if A is a subset of B, then the tool returns **B entails A** (*modus ponens*):

   e.g., *Alle bambine furono dati i regali* (The gifts were given to the girls) and *Piero ha dato i regali alle bambine* (Piero gave the gifts to the girls)
3. if no mutual or partial entailment apply, but one or more CSRs are in common, then the tool returns **No entailment, however there are common CSRs**:

   e.g., *La mamma ha fatto accompagnare il bambino dalla nonna* (The mother had her grandmother accompany the child) and *Il bambino si è fatto accompagnare dalla nonna* (The child was accompanied by his grandmother)
4. if there are no entailments and no common CSRs, the tool returns **No entailment**:

   e.g.	*Piero ha mangiato* (Piero ate) and *Luca ha dormito* (Luca slept)

### Equality of Cognate Semantic Roles

​	To assess whether a set of CSRs is a subset of another one, it is necessary to understand when two CSRs are equal. As a general rule, two CSRs are equal when the fields F1, F2 and F3 are identical. F1 is a string, F2 is an array of strings (the first element is always verbal) and F3 is a string. Most of the times F2 has length 1; however, it may contain other words, as in the following case, which permits the detection of a certain kind of entailment (which is still work in progress):

* *L'amico è stato insultato* (My friend was insulted) and *L'amico è stato preso a parolacce* (Profanities were uttered against my friend)

| Assignee | Cognate or Suppletive Assigner | Verbal Morphology | Origin of Semantic Role  | Equative Sentence                |
| -------- | ------------------------------ | ----------------- | ------------------------ | -------------------------------- |
| L'AMICO  | INSULTARE                      | PASSIVE           | Verbal (OrdinarySemRole) | L'AMICO è chi o cosa è insultato |

| Assignee | Cognate or Suppletive Assigner | Verbal Morphology | Origin of Semantic Role | Equative Sentence                |
| -------- | ------------------------------ | ----------------- | ----------------------- | -------------------------------- |
| L'AMICO  | INSULTARE, PAROLACCE           | PASSIVE           | Non-verbal (parolacce)  | L'AMICO è chi o cosa è insultato |

## Suppletion

​	The non-verbal predicate *applauso*, analyzed above, does have a verbal counterpart, i.e. the verb *applaudire*. As shown above, this makes entailment detection straightforward. However, a number of non-verbal predicates do not have a corresponding verb with the same root, as is the case, for example, with the noun *inchiesta* (inquiry; the verb *inchiedere* is obsolete): *Carlo ha fatto un'inchiesta* (Carlo did an investigation). If this is the case, a suppletive verb is used in the dictionary entry of such nouns, as shown in the following screenshot and in the ensuing analysis (this way, an entailment obtains between the sentences *Carlo ha fatto un'inchiesta* and *Carlo ha indagato* (Carlo investigated)):

```python
    # data > verb_support.py
    "inchiesta": {"verbi_supp": ["fare"], "verbo": "indagare"},
    "incursione": {"verbi_supp": ["fare"], "verbo": "penetrare"},
    # ...
```

![image-20210807102626339](README.assets/005.png)

# The label NLPytaly

​	The name given to the parser NLPytaly includes:

1. the acronym NLP, that is Natural Language Processing. Since NLP is generally data-driven, this acronym might be misleading because hitherto the tool is rule-based. Its scripts are based on our current understanding of the syntax of the clause types being analyzed;
2. the initial letters of the programming language deployed, that is Python (3.10);
3. the Italian TAL acronym, that is *Trattamento Automatico della Lingua*, i.e. one of the labels used to refer to Natural Language Processing;
4. a slightly different spelling of the country where the parsed language is spoken.
# Installation

Requirements:

* python 3.10
* virtualenv

Run the following commands:

```
git clone https://github.com/ignaziomirto2017/NLPytaly.git
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**You'll also need to provide your implementation of `request_tags` in `request_tags.py` .** Please refer to [TreeTagger website](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) for more information on how to install TreeTagger. The suggested Python wrapper is [this one](https://github.com/miotto/treetagger-python) and the parameter file used is [this one](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/italian.par.gz).

# Demo

Interested? A small playground is online at http://nlpytaly.duckdns.org. Send a mail to ignaziomauromirto@gmail.com to request free access or, alternatively, have a look at:

* [Computational linguistics/Meaning extraction - A demo of NLPytaly - Video_1: Causative sentences vs ordinary sentences | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/video/jKmV4l) (in Italian)

* [Measuring Meaning. The rationale of Semantic Role Labeling | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/video/kzMgJl)
* [Machine-readable entailments and Automatic Recognition of Paraphrases in Italian | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/video/l4wXZ1)
# References
1. Mirto, Ignazio Mauro (2022), Measuring meaning (2022), in Arai, K. (ed.), Intelligent Computing, LNNS 283, pp. 1054-1067. ISBN 978-3-030-80119-9; DOI https://doi.org/10.1007/978-3-030-80119-9
2. Mirto, Ignazio Mauro (2022), Machine-readable entailments with the Italian 'prendere' construction expressing hitting and insulting events, *International Journal on Natural Language Computing* (IJNLC) Vol.11, No.3, 17-23;[https://www.academia.edu/82516239/Machine_Readable_entailments_with_the_Italian_prendere_construction_expressing_hitting_and_insulting_events]
3. Mirto, Ignazio Mauro (2021), Automatic extraction of semantic roles in support verb constructions, *International Journal on Natural Language Computing* (IJNLC) Vol.10, No.3, 1-10; [(1) (PDF) Automatic Extraction of Semantic Roles in Support Verb Constructions | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/49054848/Automatic_Extraction_of_Semantic_Roles_in_Support_Verb_Constructions)
4. Mirto, Ignazio Mauro (2020), [Natural Language Inference in Ordinary and Support Verb Constructions](https://link.springer.com/chapter/10.1007/978-3-030-53036-5_13), in Dong *et al* (eds.), *Distributed Computing and Artificial Intelligence, 17th International Conference*, Springer Nature Switzerland, 124-133. https://link.springer.com/chapter/10.1007/978-3-030-53036-5_13
5. Mirto, Ignazio Mauro (2019), The role of cognate semantic roles: Machine Translation support for support verb constructions, [(1) (PDF) The role of cognate semantic roles: Machine translation support for support verb constructions | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/38859556/The_role_of_cognate_semantic_roles_Machine_translation_support_for_support_verb_constructions)
6. Mirto, Ignazio Mauro (2022), L'estrazione automatica dei ruoli semantici corradicali: *the importance of being cognate*, in D'Antonio, G., G. De Bueris, S. Messina and A. Scocozza (eds.), in *Comunicazione, linguaggi e società. Studi in onore di Annibale Elia*, Penguin-Random House. Grupo Editorial, Bogotà, 377-392 [(PDF) L'estrazione automatica dei ruoli semantici corradicali. The importance of being cognate | Ignazio Mauro Mirto - Academia.edu](https://www.academia.edu/39796685/Lestrazione_automatica_dei_ruoli_semantici_corradicali_The_importance_of_being_cognate)
7. Mirto, Ignazio Mauro (2007), Dream a little dream of me. Cognate predicates in English, in *Actes du 26e Colloque International Lexique-Grammaire*, Bonifacio, Corse (France), 2-6 October 2007, Camugli C., M. Constant e A. Dister (eds.), 121-128; on-line: http://infolingu.univ-mlv.fr/Colloques/Bonifacio/proceedings/mirto.pdf
