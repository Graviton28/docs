#!/usr/bin/env python3
"""Migrate UNM-CARC QuickBytes + webinfo content into the OKF/Zensical docs tree.

Reproducible pipeline:
  1. Clones (or reuses) the source repos.
  2. For every mapped file: normalizes the title, prepends OKF v0.2 frontmatter
     (type, description, tags, generated, sources w/ git last_modified, status),
     rewrites image/asset/inter-doc links, injects legacy-cluster warnings, and
     appends a human-readable provenance line.
  3. Converts Jupyter notebooks to Markdown (requires nbconvert).
  4. Copies images and downloadable assets into docs/assets/.
  5. Generates OKF §8 section index.md directory listings.

Usage:
  QB_DIR=/tmp/QuickBytes WEBINFO_DIR=/tmp/webinfo python3 scripts/migrate_quickbytes.py

Idempotent: re-running overwrites previously migrated files.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMG_DIR = DOCS / "assets" / "images" / "quickbytes"
FILES_DIR = DOCS / "assets" / "files"

QB_DIR = Path(os.environ.get("QB_DIR", ROOT / ".cache" / "QuickBytes"))
WEBINFO_DIR = Path(os.environ.get("WEBINFO_DIR", ROOT / ".cache" / "webinfo"))

QB_URL = "https://github.com/UNM-CARC/QuickBytes"
WEBINFO_URL = "https://github.com/UNM-CARC/webinfo"

GENERATED_AT = "2026-08-29T00:00:00Z"
GENERATED_BY = "claude/fable-5"
HW_STALE = "2027-08-31T00:00:00Z"  # staleness horizon for hardware-specific pages


@dataclass
class Page:
    src: str                      # path relative to source repo ("" => hand-written)
    dest: str                     # path relative to docs/
    title: str
    description: str
    type: str = "Guide"           # OKF concept type
    tags: list = field(default_factory=list)
    status: str = ""              # "", "draft", "deprecated"
    stale_after: str = ""
    repo: str = "quickbytes"      # quickbytes | webinfo | hand
    notebook: bool = False
    note: str = ""                # extra admonition inserted after the H1


# --------------------------------------------------------------------------
# Content mapping
# --------------------------------------------------------------------------

PAGES: list[Page] = [
    # ---- Getting started (hand-written pages declared for index generation)
    Page("", "getting-started/overview.md", "Getting started at CARC",
         "Create a CARC account, join a project in ColdFront, and find support.",
         "Guide", ["Accounts", "New users"], repo="hand"),
    Page("", "getting-started/good-neighbor-policy.md", "Good Neighbor Use Policy",
         "Acceptable-use rules that all CARC users agree to: account sharing, data restrictions, job monitoring, and security.",
         "Policy", ["Policy", "New users"], repo="hand"),
    Page("logging_in.md", "getting-started/logging-in.md", "Logging in to CARC systems",
         "Connect to CARC clusters with SSH from Linux, macOS, or Windows.",
         "Guide", ["SSH", "New users"]),
    Page("password_reset.md", "getting-started/password-reset.md", "Password reset and one-time passwords",
         "Reset your CARC password and manage one-time-password (OTP) settings.",
         "Guide", ["Accounts", "Security"]),
    Page("ssh_keygen_config.md", "getting-started/ssh-keys.md", "SSH keys and client configuration",
         "Generate SSH key pairs and configure your SSH client for convenient, secure logins.",
         "Guide", ["SSH", "Security"]),
    Page("X11_forwarding.md", "getting-started/x11-forwarding.md", "X11 forwarding",
         "Display graphical applications from CARC machines on your local screen with X11 forwarding.",
         "Guide", ["SSH", "Visualization"]),
    Page("transfer_data.md", "getting-started/transferring-data.md", "Transferring data",
         "Move data to and from CARC systems with scp, rsync, sftp, and Globus.",
         "Guide", ["Data", "Storage"]),
    Page("linux_intro.md", "getting-started/linux-intro.md", "Introduction to Linux",
         "A first tour of the Linux command line for new HPC users.",
         "Tutorial", ["Linux", "New users"]),
    Page("learning_linux.md", "getting-started/learning-linux.md", "Learning Linux resources",
         "Curated external resources for learning the Linux command line.",
         "Reference", ["Linux", "New users"]),

    # ---- Systems & storage
    Page("", "systems/overview.md", "Systems overview",
         "Current CARC clusters (Easley, Hopper, Xena), storage tiers, and web portals such as JupyterHub, Open OnDemand, and XDMoD.",
         "Reference", ["Systems", "Hardware"], stale_after=HW_STALE, repo="hand"),
    Page("resource_limits.md", "systems/resource-limits.md", "Storage and compute usage policies",
         "Storage quotas, Slurm fairshare policy, and per-cluster queue limits.",
         "Policy", ["Policy", "Storage", "Slurm"], stale_after=HW_STALE, repo="webinfo"),
    Page("storage_and_backup.md", "systems/storage.md", "Storage and backups",
         "CARC storage spaces (home, project, scratch), where to compute from, and what is backed up.",
         "Guide", ["Storage", "Data"]),
    Page("storage_permissions_BeeGFS.md", "systems/storage-permissions.md", "Storage permissions on BeeGFS",
         "Manage file and directory permissions, including ACLs, on CARC BeeGFS scratch storage.",
         "Guide", ["Storage", "Security"]),
    Page("systems_information.md", "systems/cluster-specifications.md", "Cluster specifications (legacy reference)",
         "Historical hardware tables for CARC clusters, including retired systems such as Wheeler, Taos, and Gibbs.",
         "Reference", ["Systems", "Hardware", "Legacy"], status="deprecated", repo="webinfo",
         note="This page is kept for history and links. Wheeler, Taos, and Gibbs have been retired — see the [Systems overview](overview.md) for current clusters."),

    # ---- Running jobs
    Page("Intro_to_slurm.md", "running-jobs/slurm-intro.md", "Introduction to Slurm",
         "Slurm basics on CARC clusters: partitions, interactive jobs, and your first batch script.",
         "Guide", ["Slurm", "Jobs", "New users"]),
    Page("submitting_jobs.md", "running-jobs/submitting-jobs.md", "Submitting jobs",
         "Submit, monitor, and cancel batch and interactive jobs with Slurm.",
         "Guide", ["Slurm", "Jobs"]),
    Page("slurm-sbatch.md", "running-jobs/slurm-reference.md", "Slurm command reference",
         "Common Slurm commands and sbatch directives with examples.",
         "Reference", ["Slurm", "Jobs"]),
    Page("submitting_sbatch_jobs.md", "running-jobs/example-slurm-scripts.md", "Example Slurm scripts",
         "Ready-to-adapt sbatch scripts for serial, parallel, and GPU jobs.",
         "Reference", ["Slurm", "Jobs", "Examples"]),
    Page("slurm_accounting.md", "running-jobs/slurm-accounting.md", "Slurm accounting and fairshare",
         "How Slurm accounts, job accounting, and the fairshare system work at CARC.",
         "Guide", ["Slurm", "Allocations"]),
    Page("pbs2slurm.md", "running-jobs/pbs-to-slurm.md", "PBS to Slurm migration",
         "Translate PBS/Torque commands and scripts to their Slurm equivalents.",
         "Reference", ["Slurm", "PBS", "Legacy"]),
    Page("module_management.md", "running-jobs/modules.md", "Environment modules",
         "Find, load, and manage software with environment modules on CARC clusters.",
         "Guide", ["Modules", "Software"]),
    Page("GNU Parallel.md", "running-jobs/gnu-parallel.md", "GNU Parallel",
         "Run many small tasks efficiently inside a single Slurm job with GNU Parallel.",
         "Guide", ["Slurm", "Parallel"]),

    # ---- Software: Python & Jupyter
    Page("anaconda_general_intro.md", "software/conda-intro.md", "Conda and Anaconda: introduction",
         "What conda is, how environments work, and how to use Anaconda/Miniconda on CARC systems.",
         "Guide", ["Python", "Conda"]),
    Page("anaconda_intro.md", "software/conda-environments.md", "Managing conda environments",
         "Create, activate, export, and remove conda environments on CARC clusters.",
         "Guide", ["Python", "Conda"]),
    Page("anaconda_pip_channels.md", "software/conda-channels-pip.md", "Conda channels and pip",
         "Use conda channels (conda-forge, bioconda) and mix pip installs safely inside environments.",
         "Guide", ["Python", "Conda"]),
    Page("Conda_JupyterHub.md", "software/conda-jupyterhub.md", "Conda environments in JupyterHub",
         "Make your conda environments available as kernels in CARC JupyterHub.",
         "Guide", ["Python", "Conda", "Jupyter"]),
    Page("Install deep learning packages.md", "software/deep-learning-packages.md", "Installing deep learning packages",
         "Install GPU-enabled deep learning frameworks (PyTorch, TensorFlow) into conda environments.",
         "Guide", ["Python", "GPU", "Machine learning"]),
    Page("parallel_jupyterhub_with_dask_and_scikit-learn.md", "software/dask-scikit-learn.md", "Parallel Python with Dask and scikit-learn",
         "Scale scikit-learn workloads across cluster nodes from JupyterHub using Dask.",
         "Tutorial", ["Python", "Jupyter", "Parallel", "Dask"]),
    Page("parallelization_with Jupyterhub_using_mpi.md", "software/jupyterhub-mpi.md", "MPI parallelization from JupyterHub",
         "Run MPI-parallel Python (mpi4py/ipyparallel) from CARC JupyterHub sessions.",
         "Tutorial", ["Python", "Jupyter", "MPI", "Parallel"]),

    # ---- Software: R
    Page("R_usage.md", "software/r-usage.md", "R on CARC systems",
         "Load R, run scripts in batch jobs, and use R interactively on CARC clusters.",
         "Guide", ["R"]),
    Page("R_at_CARC/getting_R_software.md", "software/getting-r.md", "Getting R software",
         "Available R versions and how to load them with environment modules.",
         "Guide", ["R", "Modules"]),
    Page("R_at_CARC/installing_packages.md", "software/r-packages.md", "Installing R packages",
         "Install R packages into your user library on CARC systems.",
         "Guide", ["R"]),
    Page("Parallel_R_with_Future.ipynb", "software/parallel-r-future.md", "Parallel R with the future package",
         "Parallelize R code across cores and nodes using the future framework.",
         "Tutorial", ["R", "Parallel"], notebook=True),
    Page("Gurobi optimizer with R.md", "software/gurobi-r.md", "Gurobi optimizer with R",
         "Use the Gurobi optimization solver from R on CARC clusters.",
         "Guide", ["R", "Optimization"]),
    Page("R_at_CARC/PBS_job_submission.md", "software/r-pbs-jobs.md", "R batch jobs with PBS (retired)",
         "Historical instructions for submitting R jobs with PBS/Torque, which CARC has replaced with Slurm.",
         "Guide", ["R", "PBS", "Legacy"], status="deprecated",
         note="CARC schedulers now run Slurm. See [R on CARC systems](r-usage.md) and [Example Slurm scripts](../running-jobs/example-slurm-scripts.md) instead."),

    # ---- Software: MATLAB
    Page("running_matlab_jobs.md", "software/matlab-jobs.md", "Running MATLAB jobs",
         "Run MATLAB non-interactively in Slurm batch jobs on CARC clusters.",
         "Guide", ["MATLAB", "Jobs"]),
    Page("Parallel MATLAB profile setup and batch submission.md", "software/parallel-matlab.md", "Parallel MATLAB: profile setup and batch submission",
         "Configure a cluster profile and submit parallel MATLAB jobs.",
         "Guide", ["MATLAB", "Parallel"]),
    Page("ParallelMatlabServer.md", "software/matlab-parallel-server.md", "MATLAB Parallel Server",
         "Use MATLAB Parallel Server to scale parpool jobs across multiple nodes.",
         "Guide", ["MATLAB", "Parallel"]),
    Page("Using GPUs on Xena with MATLAB.md", "software/matlab-gpu.md", "MATLAB on GPUs",
         "Accelerate MATLAB computations with GPUs on CARC clusters.",
         "Guide", ["MATLAB", "GPU"]),
    Page("MATLAB Deep Learning on Xena.md", "software/matlab-deep-learning.md", "MATLAB deep learning",
         "Train deep learning models in MATLAB using CARC GPU nodes.",
         "Tutorial", ["MATLAB", "GPU", "Machine learning"]),

    # ---- Software: AI & ML
    Page("PyTorch_1.9_Xena.md", "software/pytorch.md", "PyTorch on CARC GPUs",
         "Install and run GPU-enabled PyTorch on CARC clusters.",
         "Guide", ["Python", "GPU", "Machine learning", "PyTorch"]),
    Page("PyTorch_Classifier_Xena .ipynb", "software/pytorch-classifier.md", "PyTorch image classifier walkthrough",
         "End-to-end example: train an image classifier with PyTorch on a CARC GPU node.",
         "Tutorial", ["Python", "GPU", "Machine learning", "PyTorch"], notebook=True),
    Page("Tensorflow_documentation.md", "software/tensorflow.md", "TensorFlow on CARC GPUs",
         "Install and run GPU-enabled TensorFlow on CARC clusters.",
         "Guide", ["Python", "GPU", "Machine learning", "TensorFlow"]),
    Page("multiGPU_tensorflow_tutorial.md", "software/tensorflow-multi-gpu.md", "Multi-GPU TensorFlow",
         "Distribute TensorFlow training across multiple GPUs on a CARC node.",
         "Tutorial", ["Python", "GPU", "Machine learning", "TensorFlow"]),
    Page("alphafold.md", "software/alphafold.md", "AlphaFold",
         "Run AlphaFold protein structure prediction on CARC systems.",
         "Guide", ["Bioinformatics", "GPU", "Machine learning"]),

    # ---- Software: containers & tools
    Page("singularity-markdown-version.md", "software/singularity.md", "Singularity / Apptainer containers",
         "Build, pull, and run software containers on CARC clusters.",
         "Guide", ["Containers", "Singularity"]),
    Page("spark_tutorial.md", "software/spark.md", "Apache Spark",
         "Launch Apache Spark clusters inside Slurm allocations for large-scale data analysis.",
         "Tutorial", ["Spark", "Big data", "Parallel"]),
    Page("paraview.md", "software/paraview.md", "ParaView remote visualization",
         "Run the ParaView server on CARC compute nodes and connect from your desktop client.",
         "Guide", ["Visualization", "ParaView"]),

    # ---- Tutorials (domain applications)
    Page("GATK_QuickByte.md", "tutorials/gatk.md", "Variant calling with GATK",
         "A genomics variant-calling workflow using GATK best practices on CARC systems.",
         "Tutorial", ["Bioinformatics", "Genomics"]),
    Page("Metabarcoding.md", "tutorials/metabarcoding.md", "Metabarcoding analysis",
         "Process environmental DNA metabarcoding data on CARC clusters.",
         "Tutorial", ["Bioinformatics", "Ecology"]),
    Page("Stacks_quickbyte.md", "tutorials/stacks.md", "RAD-seq analysis with Stacks",
         "Analyze restriction-site associated DNA sequencing (RAD-seq) data with Stacks.",
         "Tutorial", ["Bioinformatics", "Genomics"]),
    Page("msprime_quickbyte.md", "tutorials/msprime.md", "Coalescent simulation with msprime",
         "Simulate genealogical histories and genome sequences with msprime.",
         "Tutorial", ["Bioinformatics", "Population genetics"]),
    Page("psmc_quickbyte.md", "tutorials/psmc.md", "Demographic inference with PSMC",
         "Infer population size history from diploid genomes using PSMC.",
         "Tutorial", ["Bioinformatics", "Population genetics"]),
    Page("Beast_at_CARC.md", "tutorials/beast.md", "Bayesian phylogenetics with BEAST",
         "Run BEAST Bayesian evolutionary analyses on CARC clusters.",
         "Tutorial", ["Bioinformatics", "Phylogenetics"]),
    Page("SimCov.md", "tutorials/simcov.md", "SimCov epidemiological simulation",
         "Run the SimCov agent-based model of SARS-CoV-2 infection dynamics in lung tissue.",
         "Tutorial", ["Simulation", "Epidemiology"]),
    Page("test_vasp_quickbyte.md", "tutorials/vasp.md", "VASP materials simulation",
         "Set up and run VASP density-functional-theory calculations on CARC clusters.",
         "Tutorial", ["Materials science", "Chemistry"]),
    Page("orca_wheeler_taos.md", "tutorials/orca.md", "ORCA quantum chemistry",
         "Run ORCA quantum chemistry calculations in parallel on CARC clusters.",
         "Tutorial", ["Chemistry"], status="draft"),
    Page("mpiCASA.md", "tutorials/mpi-casa.md", "Parallel CASA for radio astronomy",
         "Run mpiCASA for parallel radio astronomy imaging on CARC clusters.",
         "Tutorial", ["Astronomy", "MPI"]),

    # ---- Training
    Page("", "training/videos.md", "Video tutorials",
         "CARC video tutorial playlists: introduction to computing at CARC and project management in ColdFront.",
         "Reference", ["Training", "Videos"], repo="hand"),
    Page("workshop_slides.md", "training/workshops.md", "Workshops and slides",
         "Slides from CARC workshops and courses, plus how to hear about upcoming sessions.",
         "Reference", ["Training", "Workshops"]),

    # ---- Support
    Page("", "support/help.md", "Getting help",
         "Open a help ticket, email CARC support, or drop into office and consultation hours.",
         "Guide", ["Support"], repo="hand"),
    Page("", "support/acknowledging-carc.md", "Acknowledging CARC",
         "The acknowledgement statement to include in publications that used CARC resources.",
         "Policy", ["Support", "Publications"], repo="hand"),

    # ---- About
    Page("", "about/mission.md", "Mission and vision",
         "CARC's vision and mission: leading and growing the computational research community at UNM.",
         "Reference", ["About"], repo="hand"),
    Page("", "about/facilities.md", "Facilities description",
         "Boilerplate facilities description for grant proposals: clusters, storage, networking, and the data center.",
         "Reference", ["About", "Grants"], stale_after=HW_STALE, repo="hand"),
    Page("", "about/partners.md", "Partner cyberinfrastructure",
         "National and regional platforms CARC users can reach: ACCESS-CI, Jetstream2, CyVerse, and MESA.",
         "Reference", ["About", "Partners"], repo="hand"),
]

SECTIONS = {
    "getting-started": ("Getting started",
        "New to CARC? Start here: accounts, policies, logging in, and moving data."),
    "systems": ("Systems & storage",
        "CARC clusters, storage spaces, quotas, and usage policies."),
    "running-jobs": ("Running jobs",
        "Schedule and manage work on CARC clusters with Slurm."),
    "software": ("Software",
        "Language environments, machine learning frameworks, containers, and applications on CARC systems."),
    "tutorials": ("Tutorials",
        "Domain-science QuickBytes: complete worked examples from genomics to materials science."),
    "training": ("Training",
        "Workshops, courses, and video tutorials from the CARC team."),
    "support": ("Support",
        "Help tickets, office hours, and acknowledging CARC in your publications."),
    "about": ("About CARC",
        "Mission, facilities, partner cyberinfrastructure, and this documentation project."),
}

# Software section subgroups for the index page (mirrors zensical.toml nav)
SOFTWARE_GROUPS = [
    ("Python & Jupyter", ["conda-intro.md", "conda-environments.md", "conda-channels-pip.md",
                          "conda-jupyterhub.md", "deep-learning-packages.md", "dask-scikit-learn.md",
                          "jupyterhub-mpi.md"]),
    ("R", ["r-usage.md", "getting-r.md", "r-packages.md", "parallel-r-future.md", "gurobi-r.md",
           "r-pbs-jobs.md"]),
    ("MATLAB", ["matlab-jobs.md", "parallel-matlab.md", "matlab-parallel-server.md", "matlab-gpu.md",
                "matlab-deep-learning.md"]),
    ("AI & machine learning", ["pytorch.md", "pytorch-classifier.md", "tensorflow.md",
                               "tensorflow-multi-gpu.md", "alphafold.md"]),
    ("Containers & tools", ["singularity.md", "spark.md", "paraview.md"]),
]

# Extra downloadable assets: (repo-relative source, docs/assets/files-relative dest)
FILE_ASSETS = [
    ("spark/slurm-spark-submit", "spark/slurm-spark-submit"),
    ("vasp_assets/INCAR", "vasp/INCAR"),
    ("vasp_assets/KPOINTS", "vasp/KPOINTS"),
    ("vasp_assets/POSCAR", "vasp/POSCAR"),
    ("vasp_assets/README_POTCAR.md", "vasp/README_POTCAR.txt"),
    ("R_at_CARC/parallel.r", "r/parallel.r"),
    ("R_at_CARC/parallel_r.pbs", "r/parallel_r.pbs"),
    ("R_at_CARC/sequential.R", "r/sequential.R"),
    ("R_at_CARC/sequential_r.pbs", "r/sequential_r.pbs"),
    ("matlabImportWheelerProfile.pbs", "matlab/matlabImportWheelerProfile.pbs"),
    ("beginner_intro_slides_2022.pdf", "workshops/beginner_intro_slides_2022.pdf"),
]

LEGACY_RE = re.compile(r"\b(Wheeler|Taos|Gibbs)\b")
LEGACY_NOTE = ("This page mentions retired CARC systems (Wheeler, Taos, or Gibbs). "
               "The workflow remains a useful example, but verify cluster names, partitions, "
               "and module versions against the [current systems](%s).")


def sh(cmd, cwd=None) -> str:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False).stdout.strip()


def ensure_repo(path: Path, url: str):
    if not (path / ".git").exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", url, str(path)], check=True)
    # need full history for per-file last_modified
    if (path / ".git" / "shallow").exists():
        subprocess.run(["git", "-C", str(path), "fetch", "--unshallow", "-q"], check=False)


def last_modified(repo_dir: Path, rel: str) -> str:
    out = sh(["git", "log", "-1", "--format=%cI", "--", rel], cwd=repo_dir)
    return out or GENERATED_AT


def yq(s: str) -> str:
    """YAML-safe double-quoted scalar."""
    return json.dumps(s, ensure_ascii=False)


def frontmatter(p: Page, repo_dir: Path, repo_url: str) -> str:
    lines = ["---",
             f"title: {yq(p.title)}",
             f"description: {yq(p.description)}",
             f"type: {p.type}"]
    if p.tags:
        lines.append("tags:")
        lines += [f"  - {t}" for t in p.tags]
    if p.status:
        lines.append(f"status: {p.status}")
    if p.stale_after:
        lines.append(f"stale_after: {yq(p.stale_after)}")
    lines += ["generated:",
              f"  by: {yq(GENERATED_BY)}",
              f"  at: {yq(GENERATED_AT)}"]
    if p.src:
        src_url = f"{repo_url}/blob/master/{urllib.parse.quote(p.src)}"
        lines += ["sources:",
                  f"  - id: {p.repo}",
                  f"    resource: {yq(src_url)}",
                  f"    title: {yq('UNM-CARC ' + ('QuickBytes' if p.repo == 'quickbytes' else 'webinfo') + ': ' + p.src)}",
                  "    author: \"team:unm-carc\"",
                  f"    last_modified: {yq(last_modified(repo_dir, p.src))}"]
    lines.append("---")
    return "\n".join(lines) + "\n"


def convert_notebook(src: Path, slug: str) -> str:
    """Convert an .ipynb to markdown; move extracted files into the image dir."""
    outdir = Path("/tmp/nbmd") / slug
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    subprocess.run([sys.executable, "-m", "nbconvert", "--to", "markdown",
                    f"--output-dir={outdir}", f"--output={slug}", str(src)], check=True)
    md = (outdir / f"{slug}.md").read_text(encoding="utf-8")
    extracted = outdir / f"{slug}_files"
    if extracted.exists():
        target = IMG_DIR / f"{slug}_files"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(extracted, target)
        md = md.replace(f"{slug}_files/", f"../assets/images/quickbytes/{slug}_files/")
    return md


def normalize_body(md: str, p: Page, image_names: set, asset_map: dict, link_map: dict) -> str:
    # Drop a leading H1/H2 title; we re-insert a clean H1 from the mapping.
    lines = md.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^#{1,2}\s+\S", lines[0]):
        lines.pop(0)
    body = "\n".join(lines).strip("\n")

    # Rewrite image references (markdown + HTML) by basename.
    def img_sub(m):
        pre, path = m.group(1), m.group(2)
        base = urllib.parse.unquote(path.split("/")[-1].split("?")[0])
        if base in image_names:
            return f"{pre}../assets/images/quickbytes/{urllib.parse.quote(base)}"
        return m.group(0)

    body = re.sub(r"(!\[[^\]]*\]\()\s*([^)\s]+)", img_sub, body)
    body = re.sub(r"(<img[^>]*\bsrc=[\"'])([^\"']+)", img_sub, body)

    # Rewrite links to bundled downloadable assets by basename.
    def asset_sub(m):
        pre, path = m.group(1), m.group(2)
        base = urllib.parse.unquote(path.split("/")[-1].split("?")[0])
        if base in asset_map and not path.startswith(("http://", "https://", "#")):
            return f"{pre}../assets/files/{asset_map[base]}"
        return m.group(0)

    body = re.sub(r"((?<!\!)\[[^\]]*\]\()\s*([^)\s]+)", asset_sub, body)

    # Rewrite inter-QuickByte links (local relative or GitHub blob URLs).
    def link_sub(m):
        pre, path = m.group(1), m.group(2)
        raw = urllib.parse.unquote(path.split("?")[0])
        base = raw.split("#")[0].split("/")[-1]
        frag = "#" + raw.split("#")[1] if "#" in raw else ""
        if base in link_map:
            target = link_map[base]
            here = str(Path(p.dest).parent)
            rel = os.path.relpath(target, here).replace(os.sep, "/")
            return f"{pre}{rel}{frag}"
        return m.group(0)

    body = re.sub(r"((?<!\!)\[[^\]]*\]\()\s*([^)\s]+)", link_sub, body)

    # Build the final document.
    out = [f"# {p.title}", ""]
    notes = []
    if p.note:
        notes.append(p.note)
    elif p.status != "deprecated" and LEGACY_RE.search(body):
        rel_overview = os.path.relpath("systems/overview.md", str(Path(p.dest).parent)).replace(os.sep, "/")
        notes.append(LEGACY_NOTE % rel_overview)
    for n in notes:
        kind = "warning" if p.status in ("deprecated", "draft") else "note"
        title = "Legacy content" if "retired" in n else "Please note"
        out.append(f'!!! {kind} "{title}"')
        out += [f"    {line}" for line in n.splitlines()]
        out.append("")
    out.append(body)
    return "\n".join(out).rstrip() + "\n"


def provenance_footer(p: Page, repo_url: str, repo_dir: Path) -> str:
    if not p.src:
        return ""
    date = last_modified(repo_dir, p.src)[:10]
    url = f"{repo_url}/blob/master/{urllib.parse.quote(p.src)}"
    return (f"\n<p class=\"carc-provenance\" markdown>Migrated from "
            f"[UNM-CARC QuickBytes]({url}) (last source update {date}). "
            f"Spotted a problem? [Open an issue or pull request]({QB_URL}).</p>\n")


def write_index(section: str, pages_by_dest: dict):
    name, blurb = SECTIONS[section]
    lines = [f"# {name}", "", blurb, ""]

    def entry(fname: str) -> str:
        p = pages_by_dest[f"{section}/{fname}"]
        suffix = " *(legacy)*" if p.status == "deprecated" else ""
        return f"* [{p.title}]({fname}) - {p.description}{suffix}"

    if section == "software":
        for group, files in SOFTWARE_GROUPS:
            lines += [f"## {group}", ""]
            lines += [entry(f) for f in files]
            lines.append("")
    else:
        ordered = [d for d in pages_by_dest if d.startswith(section + "/")]
        lines += [entry(d.split("/", 1)[1]) for d in ordered]
        lines.append("")
    if section == "about":
        lines += ["* [Documentation update log](../log.md) - Chronological history of changes to this documentation bundle.", ""]
    (DOCS / section / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    ensure_repo(QB_DIR, QB_URL)
    ensure_repo(WEBINFO_DIR, WEBINFO_URL)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    FILES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy images (Images/ dir + every root-level png/jpeg/jpg/gif).
    image_names = set()
    img_src = []
    imgdir = QB_DIR / "Images"
    if imgdir.exists():
        img_src += sorted(imgdir.iterdir())
    img_src += sorted(QB_DIR.glob("*.png")) + sorted(QB_DIR.glob("*.jpeg")) + \
               sorted(QB_DIR.glob("*.jpg")) + sorted(QB_DIR.glob("*.gif"))
    for f in img_src:
        if f.is_file():
            shutil.copy2(f, IMG_DIR / f.name)
            image_names.add(f.name)

    # 2. Copy downloadable assets.
    asset_map = {}
    for src, dest in FILE_ASSETS:
        s = QB_DIR / src
        if s.exists():
            d = FILES_DIR / dest
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            asset_map[Path(src).name] = dest
    # workshop slide decks
    ws = QB_DIR / "workshop_slides"
    if ws.exists():
        for f in sorted(ws.glob("*.pdf")):
            d = FILES_DIR / "workshops" / f.name
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, d)
            asset_map[f.name] = f"workshops/{f.name}"

    # 3. Link map: source basename -> docs-relative dest (also html twins).
    link_map = {}
    for p in PAGES:
        if p.src:
            base = Path(p.src).name
            link_map[base] = p.dest
            if base.endswith(".md"):
                link_map[base[:-3] + ".html"] = p.dest

    pages_by_dest = {p.dest: p for p in PAGES}

    # 4. Migrate.
    migrated, skipped = [], []
    for p in PAGES:
        if p.repo == "hand":
            continue
        repo_dir = QB_DIR if p.repo == "quickbytes" else WEBINFO_DIR
        repo_url = QB_URL if p.repo == "quickbytes" else WEBINFO_URL
        src = repo_dir / p.src
        if not src.exists():
            skipped.append(p.src)
            continue
        if p.notebook:
            slug = Path(p.dest).stem
            raw = convert_notebook(src, slug)
        else:
            raw = src.read_text(encoding="utf-8", errors="replace")
        body = normalize_body(raw, p, image_names, asset_map, link_map)
        doc = frontmatter(p, repo_dir, repo_url) + "\n" + body + provenance_footer(p, repo_url, repo_dir)
        dest = DOCS / p.dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(doc, encoding="utf-8")
        migrated.append(p.dest)

    # 5. Section indexes (OKF §8: no frontmatter, heading + bullet listings).
    for section in SECTIONS:
        write_index(section, pages_by_dest)

    print(f"Migrated {len(migrated)} pages; copied {len(image_names)} images, "
          f"{len(asset_map)} downloadable assets.")
    if skipped:
        print("MISSING SOURCES:")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
