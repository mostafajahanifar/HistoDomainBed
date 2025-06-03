# 🧪 HistoDomainBed

> A comparative benchmarking framework for **Domain Generalization** in **Computational Pathology**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Built on DomainBed](https://img.shields.io/badge/Built%20on-DomainBed-ff69b4)](https://github.com/facebookresearch/DomainBed)

---

**HistoDomainBed** is an open-source extension of the [DomainBed](https://github.com/facebookresearch/DomainBed) framework, specifically adapted for the **computational pathology (CPath)** domain. It provides a rigorous and reproducible pipeline for evaluating **domain generalization (DG)** algorithms on pathology image classification tasks, including support for stain augmentation, self-supervised pretrained models initialization, histopathology image dataset, F1 score for evaluation, and more.

📌 **Main paper**: [_Comparative Benchmarking of Domain Generalization in Computational Pathology_](https://arxiv.org/abs/2409.17063)  
📁 **Dataset**: [HistoPANTUM Dataset](https://zenodo.org/records/14555794)  
🧠 **Built on top of**: [DomainBed (Facebook AI Research)](https://github.com/facebookresearch/DomainBed)  
📊 **Comprehensive experiment logging and reproducibility** including 7,560+ runs across algorithms/tasks/settings
![full_domains_f1](https://github.com/user-attachments/assets/4d9e13b2-0b6c-44d9-95c1-dfd17e3dbddc)


---

## 🧬 The HistoPANTUM Dataset

The **HistoPANTUM dataset** is a curated, multi-center TCGA-based dataset for tumor vs. non-tumor classification, designed to introduce **realistic domain shifts** across tissue source sites. It is annotated by an expert pathologist and consists of image patches from clearly distinguishable tumor and non-tumor regions.

- 🧠 Task: Binary classification (tumor vs. non-tumor)
- 🏥 Domains: Different tumor sites (cancer types)
- 🖼️ Images: 140,569 H&E-stained tiles of 224 × 224 pixels (approximately 1 mpp resolution)
- 📤 Download: [Zenodo – HistoPANTUM](https://zenodo.org/records/14555794)

### 📁 Dataset Directory Structure

To use any dataset with **HistoDomainBed**, organize it as follows:

```bash
/data/
└── HistoPANTUM/
    ├── colon/              # Domain 1
    │   ├── tumor/
    │   │   ├── img001.png
    │   │   ├── img002.png
    │   └── non_tumor/
    │       ├── img003.png
    │       ├── img004.png
    ├── ovarian/              # Domain 2
    │   ├── tumor/
    │   └── non_tumor/
    └── stomach/              # Domain 3
        ├── tumor/
        └── non_tumor/
```
Each dataset should follow this hierarchy:  
🔹 Top-level folder: Name of the dataset (✅ Compatible datasets: HISTOPANTUM, MIDOG, CAMELYON)  
🔹 Subfolders: Each domain (typically a source site or hospital)  
🔹 Sub-subfolders: Each class (e.g., tumor, non_tumor)  
This structure enables HistoDomainBed to automatically identify domains and class labels for DG training and evaluation.

---

## 🏗️ Architecture and Design

HistoDomainBed is a **extension of DomainBed**, tailored to CPath:

- 🏛️ **Backbone**: ResNet-50 (fixed for fair comparison)
- 🧪 **Tasks**: : Metastasis Detection (CAMELYON dataset), Mitosis Detection (MIDOG22 dataset), and Tumor Detection (HistoPANTUM)
- 🧠 **DG Algorithms**: DomainBed Algorithms (see below) + BT-TCGA (ERM model weights initialized with Barlow Twins pretrained on TCGA taken from [lunit-io/benchmark-ssl-pathology](https://github.com/lunit-io/benchmark-ssl-pathology)) + Stain Augmentation (ERM with [Stain Augmentation](https://tia-toolbox.readthedocs.io/en/v1.6.0/_autosummary/tiatoolbox.tools.stainaugment.StainAugmentor.html)) + Stain Normalization (this one is just ERM used on normalized images using [Macenko algorithm](https://tia-toolbox.readthedocs.io/en/latest/_autosummary/tiatoolbox.tools.stainnorm.MacenkoNormalizer.html))

The [currently available algorithms](domainbed/algorithms.py) are:

* Empirical Risk Minimization (ERM, [Vapnik, 1998](https://www.wiley.com/en-fr/Statistical+Learning+Theory-p-9780471030034))
* Invariant Risk Minimization (IRM, [Arjovsky et al., 2019](https://arxiv.org/abs/1907.02893))
* Group Distributionally Robust Optimization (GroupDRO, [Sagawa et al., 2020](https://arxiv.org/abs/1911.08731))
* Interdomain Mixup (Mixup, [Yan et al., 2020](https://arxiv.org/abs/2001.00677))
* Marginal Transfer Learning (MTL, [Blanchard et al., 2011-2020](https://arxiv.org/abs/1711.07910))
* Meta Learning Domain Generalization (MLDG, [Li et al., 2017](https://arxiv.org/abs/1710.03463))
* Maximum Mean Discrepancy (MMD, [Li et al., 2018](https://openaccess.thecvf.com/content_cvpr_2018/papers/Li_Domain_Generalization_With_CVPR_2018_paper.pdf))
* Deep CORAL (CORAL, [Sun and Saenko, 2016](https://arxiv.org/abs/1607.01719))
* Domain Adversarial Neural Network (DANN, [Ganin et al., 2015](https://arxiv.org/abs/1505.07818))
* Conditional Domain Adversarial Neural Network (CDANN, [Li et al., 2018](https://openaccess.thecvf.com/content_ECCV_2018/papers/Ya_Li_Deep_Domain_Generalization_ECCV_2018_paper.pdf))
* Style Agnostic Networks (SagNet, [Nam et al., 2020](https://arxiv.org/abs/1910.11645))
* Adaptive Risk Minimization (ARM, [Zhang et al., 2020](https://arxiv.org/abs/2007.02931)), contributed by [@zhangmarvin](https://github.com/zhangmarvin)
* Variance Risk Extrapolation (VREx, [Krueger et al., 2020](https://arxiv.org/abs/2003.00688)), contributed by [@zdhNarsil](https://github.com/zdhNarsil)
* Representation Self-Challenging (RSC, [Huang et al., 2020](https://arxiv.org/abs/2007.02454)), contributed by [@SirRob1997](https://github.com/SirRob1997)
* Spectral Decoupling (SD, [Pezeshki et al., 2020](https://arxiv.org/abs/2011.09468))
* Learning Explanations that are Hard to Vary (AND-Mask, [Parascandolo et al., 2020](https://arxiv.org/abs/2009.00329))
* Out-of-Distribution Generalization with Maximal Invariant Predictor (IGA, [Koyama et al., 2020](https://arxiv.org/abs/2008.01883))
* Gradient Matching for Domain Generalization (Fish, [Shi et al., 2021](https://arxiv.org/pdf/2104.09937.pdf))
* Self-supervised Contrastive Regularization (SelfReg, [Kim et al., 2021](https://arxiv.org/abs/2104.09841))
* Smoothed-AND mask (SAND-mask, [Shahtalebi et al., 2021](https://arxiv.org/abs/2106.02266))
* Invariant Gradient Variances for Out-of-distribution Generalization (Fishr, [Rame et al., 2021](https://arxiv.org/abs/2109.02934))
* Learning Representations that Support Robust Transfer of Predictors (TRM, [Xu et al., 2021](https://arxiv.org/abs/2110.09940))
* Invariance Principle Meets Information Bottleneck for Out-of-Distribution Generalization (IB-ERM , [Ahuja et al., 2021](https://arxiv.org/abs/2106.06607))
* Invariance Principle Meets Information Bottleneck for Out-of-Distribution Generalization (IB-IRM, [Ahuja et al., 2021](https://arxiv.org/abs/2106.06607))
* Optimal Representations for Covariate Shift (CAD & CondCAD, [Ruan et al., 2022](https://arxiv.org/abs/2201.00057)), contributed by [@ryoungj](https://github.com/ryoungj)
* Quantifying and Improving Transferability in Domain Generalization (Transfer, [Zhang et al., 2021](https://arxiv.org/abs/2106.03632)), contributed by [@Gordon-Guojun-Zhang](https://github.com/Gordon-Guojun-Zhang)
* Invariant Causal Mechanisms through Distribution Matching (CausIRL with CORAL or MMD, [Chevalley et al., 2022](https://arxiv.org/abs/2206.11646)), contributed by [@MathieuChevalley](https://github.com/MathieuChevalley)
* Empirical Quantile Risk Minimization (EQRM, [Eastwood et al., 2022](https://arxiv.org/abs/2207.09944)), contributed by [@cianeastwood](https://github.com/cianeastwood)


---

## 🚀 Getting Started

Train a model:

```sh
python3 -m domainbed.scripts.train\
       --data_dir=./domainbed/data/MNIST/\
       --algorithm IGA\
       --dataset ColoredMNIST\
       --test_env 2
```

Launch a sweep:

```sh
python -m domainbed.scripts.sweep launch\
       --data_dir=/my/datasets/path\
       --output_dir=/my/sweep/output/path\
       --command_launcher MyLauncher
```

Here, `MyLauncher` is your cluster's command launcher, as implemented in `command_launchers.py`. At the time of writing, the entire sweep trains tens of thousands of models (all algorithms x all datasets x 3 independent trials x 20 random hyper-parameter choices). You can pass arguments to make the sweep smaller on histopathology dataset only:

```sh
python -m domainbed.scripts.sweep launch\
       --data_dir=/my/datasets/path\
       --output_dir=/my/sweep/output/path\
       --command_launcher MyLauncher\
       --algorithms ERM DANN\
       --datasets HISTOPANTUM MIDOG\
       --n_hparams 3\
       --n_trials 3
```

After all jobs have either succeeded or failed, you can delete the data from failed jobs with ``python -m domainbed.scripts.sweep delete_incomplete`` and then re-launch them by running ``python -m domainbed.scripts.sweep launch`` again. Specify the same command-line arguments in all calls to `sweep` as you did the first time; this is how the sweep script knows which jobs were launched originally.

To view the results of your sweep:

````sh
python -m domainbed.scripts.collect_results\
       --input_dir=/my/sweep/output/path
````

## License

This source code is released under the MIT license, included [here](LICENSE).
