<h1 align="center">Sapphire</h1>

<p align="center"> An assistant for managing and talking to your directories. </p>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#roadmap">Roadmap</a>
</p>

<div align="center">
    <br />

    [![license](https://img.shields.io/github/license/dec0dOS/amazing-github-template.svg?style=flat-square)](LICENSE)
</div>

## Features
The app contains two agents: the 🦉 Wizard 🦉 and the 🔮 Witch 🔮. It's mainly for personal use with [Obsidian](https://obsidian.md) for classes...

### 🦉 Wizard 🦉
TODO: insert demo

- Request an action to be done to your current directory. The wizard will execute the corrseponding command for you.
- Examples of requests: 
  - List the files that were created after September 22, 2022.
  - Replace all instances of "witch" in ./sorcery with "wizard".
  - etc.

### 🔮 Witch 🔮
TODO: insert demo

- Ask the witch a question about the contents of the files in your current directory. The witch will intelligently answer your question using the knowledge obtained from your files.
- Note: as of now, only markdown features are supported.
- Examples of questions (given the directory contains notes about [computational photography](https://courses.engr.illinois.edu/cs445/fa2023/)):
  - What did the professor say are the tradeoffs between Lagrangian vs Eulerian motion magnification in videos?
  - How does Laplacian pyramid blending work?
  - Which of the following properties apply to affine transformations? [...]
  - etc.

## Usage
1. Clone the repo
2. Store your [Open AI key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) as an environment variable called `OPENAI_API_KEY`
3. Add an alias for `/src/main.py` to your `.bashrc` so that you can call Sapphire from any directory
  1. For me, this looked like `alias sapphire='python [my_path]/sapphire/src/main.py'`
4. `cd` into the cloned repo and run `pip install -r requirements.txt`

## Roadmap
- [ ] Fix manual data reingestion—see [open issue T_T](https://github.com/langchain-ai/langchain/issues/14872)
- [ ] Ingest images
- [ ] Improve console styling
- [ ] Support Latex
