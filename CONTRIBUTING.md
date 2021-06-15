# Contributing to GSwidgetkit

Thanks for taking the time to contribute. We're excited to have you!

GS widgetkit is a wxPython extension library originally created for use in Gimel Studio and the same forums, etc can be used to discuss GS widgetkit.

The following is a set of guidelines for contributing to GS widgetkit, which is hosted in the [Github Organization](https://github.com/GimelStudio) as part of Gimel Studio on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

Read the following sections in order to know how to ask questions and how to work on something in an orderly manner.

GS widgetkit is an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, bug reports and feature requests or writing code which can be incorporated into GS widgetkit itself.


#### Table Of Contents

[Asking for help](#asking-for-help)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Technical](#technical)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Your First Code Contribution](#your-first-code-contribution)

[Styleguides](#styleguides)


## Asking For Help

**Please, don't use the issue tracker for general support questions, etc**. Check whether the channels on the official [Discord](https://discord.gg/RqwbDrVDpK) or [Gitter](https://gitter.im/Gimel-Studio/community) can help with your issue. Discord is where most of the development chat happens and it's likely you will get your answer the quickest there.


## What Should I Know Before I Get Started?

### Technical

GS widgetkit itself is written in pure Python so most code contributions will require at least a basic knowledge of Python 3+. Since GS widgetkit is an extension library of wxPython, a basic knowledge of [wxPython](https://wxpython.org) is really essential.


## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for GS widgetkit. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

When you are creating a bug report, please include as many details as possible. Fill out the template as the information it asks for helps us resolve issues faster.

#### Before Submitting A Bug Report

Make sure to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). After you've determined  your bug is related to, create an issue in the repository and provide as much helpful information as you can to help us understand the problem.

### Your First Code Contribution

Unsure where to begin contributing to GS widgetkit? You can start by looking through these `good-first-issue` and `help-wanted` issues:

* [Good First issues](https://github.com/GimelStudio/gswidgetkit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - issues which should only require a few lines of code and/or don't require an in-depth knowledge of the existing code.
* [Help wanted issues](https://github.com/GimelStudio/gswidgetkit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) - issues which should be a bit more involved.

Both issue lists are sorted by total number of comments. While not perfect, number of comments is a reasonable proxy for impact a given change will have.

If you have any questions about contributing, feel free to ask on the official [Discord](https://discord.gg/RqwbDrVDpK) or [Gitter](https://gitter.im/Gimel-Studio/community).


## Styleguides

### Git Commit Messages

* Use the present tense ("add feature" not "added feature")
* Use all lowercase except for referencing a file, method, function, class, etc in the code
* Use the imperative mood ("move cursor to..." not "moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Python Code

Python code should largely follow PEP8 guidlines, except:

* The line length can be greater than the PEP8 character limit
* Capitalization of function and method names are acceptable since this is the style used in wxPython (the GUI library).

### Python File Naming Conventions

* Python file names should use "snake case" and no capital letters (``nodegraph_pnl`` not ``nodegraphpnl``)
