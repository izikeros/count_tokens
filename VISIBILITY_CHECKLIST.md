# Project Visibility Checklist

A comprehensive checklist to maximize project discoverability across GitHub, search engines, package registries, and social media.

## GitHub Repository Optimization

### Repository Settings
- [ ] **Description**: Short, keyword-rich description (appears in search results)
- [ ] **Topics/Tags**: Add 5-10 relevant topics (e.g., `python`, `library`, `cli`, domain-specific tags)
- [ ] **Website URL**: Link to documentation site (izikeros.github.io/count_tokens)
- [ ] **Social preview image**: Custom image for link sharing (1280×640px recommended)
- [ ] **Sponsor button**: Configure if accepting sponsorships

### Repository Files
- [ ] **README.md**: Comprehensive with badges, examples, installation instructions
- [ ] **LICENSE**: MIT license file present
- [ ] **CONTRIBUTING.md**: Guidelines for contributors
- [ ] **CODE_OF_CONDUCT.md**: Community standards
- [ ] **SECURITY.md**: Security policy and vulnerability reporting
- [ ] **CHANGELOG.md**: Release history maintained

### GitHub Features
- [ ] **Issue templates**: Bug report and feature request templates
- [ ] **PR template**: Pull request template
- [ ] **Discussions**: Enable for community Q&A (optional)
- [ ] **GitHub Pages**: Documentation deployed
- [ ] **Releases**: Tagged releases with release notes

## README Excellence

### Structure
- [ ] **Project name and tagline**: Clear, memorable, describes purpose
- [ ] **Badges**: CI status, coverage, PyPI version, license, downloads
- [ ] **Installation**: pip/uv install command
- [ ] **Quick start**: Minimal code example that works
- [ ] **Features list**: Key capabilities
- [ ] **Documentation link**: Link to full docs
- [ ] **Contributing section**: How to contribute
- [ ] **License section**: License type

### Badge Examples
```markdown
[![CI](https://github.com/izikeros/count_tokens/actions/workflows/ci.yml/badge.svg)](https://github.com/izikeros/count_tokens/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/izikeros/count_tokens/branch/main/graph/badge.svg)](https://codecov.io/gh/izikeros/count_tokens)
[![PyPI version](https://badge.fury.io/py/count-tokens.svg)](https://badge.fury.io/py/count-tokens)
[![Downloads](https://pepy.tech/badge/count-tokens)](https://pepy.tech/project/count-tokens)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://izikeros.github.io/count_tokens)
```

## Package Registry (PyPI)

- [ ] **Package published**: Available on PyPI
- [ ] **Description**: Clear, searchable description in pyproject.toml
- [ ] **Keywords**: Relevant keywords in pyproject.toml
- [ ] **Classifiers**: Proper classifiers for categorization
- [ ] **Project URLs**: Homepage, documentation, repository, changelog
- [ ] **Long description**: README renders properly on PyPI

### Optional Registries
- [ ] **Conda-forge**: Submit recipe for conda users
- [ ] **TestPyPI**: Test releases before production

## Documentation Site

- [ ] **Landing page**: Clear value proposition
- [ ] **Getting started guide**: Step-by-step tutorial
- [ ] **API reference**: Auto-generated from docstrings
- [ ] **Examples/Tutorials**: Real-world use cases
- [ ] **Changelog**: Linked or embedded
- [ ] **Search**: Enabled in mkdocs
- [ ] **Mobile-friendly**: Responsive design

## Social Media & Community Promotion

### Announcement Channels
- [ ] **Personal blog**: Write announcement post on safjan.com
- [ ] **Twitter/X**: Tweet with relevant hashtags (#Python, #OpenSource)
- [ ] **LinkedIn**: Professional announcement post
- [ ] **Reddit**: Post to r/Python (follow rules, no spam)
- [ ] **Hacker News**: Submit if project is substantial/novel
- [ ] **Dev.to**: Write tutorial or announcement article
- [ ] **Mastodon**: Post to Python community

### Newsletter Submissions
- [ ] **Python Weekly**: Submit to pythonweekly.com
- [ ] **Awesome Python**: Submit PR if fits a category
- [ ] **PyCoder's Weekly**: Submit to pycoders.com

### Community Engagement
- [ ] **Stack Overflow**: Answer questions using your library
- [ ] **GitHub Discussions**: Engage with users
- [ ] **Discord/Slack**: Share in relevant Python communities

## SEO & Discoverability

- [ ] **Package name**: Unique, searchable, memorable
- [ ] **Keywords**: Used consistently in description, README, docs
- [ ] **Backlinks**: Link from personal site, other projects
- [ ] **Google indexing**: Verify docs site is indexed

## Quality Signals

### Maintenance Indicators
- [ ] **Regular releases**: Show active development
- [ ] **Issue response time**: Respond promptly to issues
- [ ] **PR reviews**: Review and merge contributions
- [ ] **Dependencies updated**: Keep dependencies current

### Code Quality
- [ ] **Test coverage**: High coverage percentage
- [ ] **Type hints**: Fully typed codebase
- [ ] **Documentation**: Complete docstrings
- [ ] **Linting**: Clean ruff/mypy output

## Metrics to Track

- **GitHub Stars**: Repository popularity
- **PyPI Downloads**: Package adoption
- **GitHub Traffic**: Views and clones
- **Documentation visits**: Page views on docs site
- **Issue activity**: Community engagement

## Post-Launch Checklist

After initial release:
- [ ] Monitor GitHub issues for bugs/questions
- [ ] Track PyPI download statistics
- [ ] Respond to community feedback
- [ ] Plan next release based on feedback
- [ ] Update documentation based on FAQs

---

## AI-Generated Visibility Helper

Ask an AI assistant to generate `.visibility-helper.md` with:
- GitHub topics suggestions
- Repository description variants
- Social preview image prompts (DALL-E/Midjourney)
- VHS tape script for terminal demo GIF
- Social media post templates
- Blog post outline

The file is git-ignored and serves as a working document for promotion tasks.

**To generate**: Ask "Help me with project visibility" or "Generate visibility helper"

---

*Last updated: 2026-02-02*
*Author: [Krystian Safjan](https://safjan.com)*
