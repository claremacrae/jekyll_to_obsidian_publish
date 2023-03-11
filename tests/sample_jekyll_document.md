---
layout: default
title: Statuses
nav_order: 2
parent: Getting Started
has_toc: false
has_children: true
---

# Statuses
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

---

## Another heading block, this time with no horizontal rule

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Introduction

{: .released }
Custom Statuses were introduced in Tasks 1.23.0.

This page provides an overview of using Tasks with **Custom Statuses**, which some people refer to as Custom Checkboxes or Alternative/Alternate Checkboxes.

Here's the kind of thing that you can do:

![Selection of checkboxes from Minimal theme](../images/theme-minimal-reading-view-sample.png) ![Selection of checkboxes from ITS theme](../images/theme-its-reading-view-sample.png)

### Related pages

Once you're comfortable with the background information in this page, further information is available in the following related pages.

- [How to style custom statuses]({{ site.baseurl }}{% link how-to/style-custom-statuses.md %}).
- [How to set up your custom statuses]({{ site.baseurl }}{% link how-to/set-up-custom-statuses.md %}).
- [Status Collections]({{ site.baseurl }}{% link reference/status-collections/index.md %}).

---

## Do I need to set up statuses?

If you are happy with all your tasks beginning with `[ ]` and `[x]`, then **no**, you can just ignore Tasks' Statuses facility.

---

## About Statuses

### What IS a Status?

Every task in the Tasks plugin now has a Status.

Status is just Tasks' name for:

1. the character (`symbol`) between the `[` and `]` in a task line
2. AND some options that you can customise, to tell tasks how to treat all your tasks with that character.

Some obsidian users call them other names, like 'Alternative Checkboxes', but that is more about how they are displayed, rather than about the actual *behaviour* of tasks with particular statuses.

### What's IN a Status?

These are the options that you can modify, for each status:

![Task Status modal](../images/settings-custom-statuses-dialog-2.png)

Here is some more detail.

- **Status Symbol**
  - the single character in the `[]` at the start of the task.
  - this character will control what how tasks are rendered by your Theme or CSS Snippet.
- **Status Name**
  - a name for the status.
  - this is flexible: for custom statuses, you can use any name you wish.
  - is searchable with `status.name`, for example `status.name includes My custom in-progress status`.
- **Next Status Symbol**
  - the status symbol to use when the task is toggled.
- **Status Type**
  - one of `TODO`, `IN_PROGRESS`, `DONE`, `CANCELLED`, `NON_TASK`.
  - Tasks needs to know the type of each status, so that it knows how to treat them when searching, and what to do when tasks with the status are toggled.
  - types are searchable with `status.type`, for example `status.type is IN_PROGRESS`.
  - Also available:
    - `sort by status.type`
    - `group by status.type`
  - For more information, see [Status Types]({{ site.baseurl }}{% link getting-started/statuses/status-types.md %})

### Unknown Statuses

What happens if Tasks reads a line with a status symbol that it does not know about?

All such tasks are given a status called `Unknown`, with these properties:

| Property           | Value                                                               |
| ------------------ | ------------------------------------------------------------------- |
| Status Symbol      | The unrecognised character between the `[` and `]` in the task line |
| Status Name        | **Unknown**                                                         |
| Next Status Symbol | `x`                                                                 |
| Status Type        | `TODO`                                                              |

### Done date, Recurrence and Statuses

It is the Task Status Type changing **to** `DONE` that controls when:

- tasks **gain** their Done dates (if Done dates are enabled in settings),
- new copies of recurring tasks are created.

It is the Task Status Type changing **from** `DONE` that controls when:

- tasks **lose** their Done dates (if Done dates are enabled in settings).

---

## What can Statuses do?

Now we have seen what is in a Status, what can we do with them?

We can use them to control what Tasks does when a task's checkbox is clicked, or toggled.

The [Example Statuses]({{ site.baseurl }}{% link getting-started/statuses/example-statuses.md %}) page has a variety of examples, for inspiration.

---

## More about Statuses

### Core Statuses

Core statuses represent conventional markdown tasks:

```text
- [ ] I am a task that is not yet done
- [x] I am a task that has been done
```

They don't require any custom CSS styling or theming on order to display correctly in Tasks blocks or Live Preview.

Before Tasks 1.23.0, these were the only statuses that Tasks knew about.

See [Core Statuses]({{ site.baseurl }}{% link getting-started/statuses/core-statuses.md %}) to find out more.

### Custom Statuses

Custom statuses represent any non-standard markdown tasks.

Here are some tasks with example custom statuses, that is, with non-standard characters between the `[` and `]`:

```text
- [X] Checked
- [-] A dropped/cancelled task
- [?] A question
- [/] A Half Done/In-progress task
```

They **require custom CSS styling or theming** on order to display correctly in Tasks blocks or Live Preview.

### What's the Big Deal?

People have been using themes and CSS snippets to style custom checkboxes in Obsidian all along.

What Tasks's custom statuses allow you to do is to **also customise the behaviour of your tasks**.

### Setting up Custom Statuses

<!-- force a blank line --> <!-- include: snippet-statuses-overview.md -->

{: .info }
> Broad steps to understand and set up Statuses (or "Alternate Checkboxes"):
>
> - Understand what Statuses are:
>   - [Statuses]({{ site.baseurl }}{% link getting-started/statuses.md %})
>   - [Custom Statuses]({{ site.baseurl }}{% link getting-started/statuses/custom-statuses.md %})
> - Choose your status styling scheme: this will determine the names and symbols for your custom statuses:
>   - Some common ones are shown in [Status Collections]({{ site.baseurl }}{% link reference/status-collections/index.md %})
> - Set up your status styling scheme
>   - [How to style custom statuses]({{ site.baseurl }}{% link how-to/style-custom-statuses.md %}).
> - Configure Tasks to use your custom statuses
>   - [How to set up your custom statuses]({{ site.baseurl }}{% link how-to/set-up-custom-statuses.md %})
> - Optionally, update your tasks searches to take advantage of the new flexibility
>   - [Filters for Task Statuses]({{ site.baseurl }}{% link queries/filters.md %}#filters-for-task-statuses)

<!-- force a blank line --> <!-- endInclude -->

---

## Using Statuses

### Editing your tasks

The [‘Create or edit Task’ Modal]({{ site.baseurl }}{% link getting-started/create-or-edit-task.md %}#status-and-done-on) allows you to change the status of a task.

### Related commands

{: .info }
There are not yet any new commands for applying custom statuses.
We are tracking this in [issue #1486](https://github.com/obsidian-tasks-group/obsidian-tasks/issues/1486) .

### Related searches

- `done` - matches tasks status types `TODO` and `CANCELLED`
- `not done` - matches tasks with status types `TODO` and `IN_PROGRESS`
- **Status Name**
  - `status.name` text search
  - `sort by status.name`
  - `group by status.name`
- **Status Type**
  - `status.type` text search
  - `sort by status.type`
  - `group by status.type`

For details, see [Filters for Task Statuses]({{ site.baseurl }}{% link queries/filters.md %}#filters-for-task-statuses)

{: .info }
We envisage adding `status.symbol`.

---

## Credit: Sytone and the 'Tasks SQL Powered' plugin

This plugin's implementation of reading, searching and editing custom statuses was entirely made possible by the work of [Sytone](https://github.com/sytone) and his fork of Tasks called ['Tasks SQL Powered'](https://github.com/sytone/obsidian-tasks-x). [^task-x-version]

Where code in Tasks has been copied from 'Tasks SQL Powered', Sytone has been specifically credited as a co-author, that is, joint author, and these commits can be seen on the GitHub site: [Commits "Co-Authored-By: Sytone"](https://github.com/search?q=repo%3Aobsidian-tasks-group%2Fobsidian-tasks+%22Co-Authored-By%3A+Sytone%22&type=commits).

Subsequently, the custom statuses implementation in Tasks has diverged from the 'Tasks SQL Powered' significantly. However, none of the new features and fixes would have been possible without Sytone's foundation work, for which we are very grateful.

[^task-x-version]: 'Tasks SQL Powered' as of [revision 2c0b659](https://github.com/sytone/obsidian-tasks-x/tree/2c0b659457cc80806ff18585c955496c76861b87) on 2 August 2022

## Extra test samples

{: .warning }
> This is a test warning

2 links on one line:
Urgency can only consider the parameters it knows: [dates]({{ site.baseurl }}{% link getting-started/dates.md %}) and [priorities]({{ site.baseurl }}{% link getting-started/priority.md %}).

Or you can read about [Status Settings]({{ site.baseurl }}{% link getting-started/statuses/status-settings.md %}), and see how to [edit a Status]({{ site.baseurl }}{% link getting-started/statuses/editing-a-status.md %}).

See [recurring tasks (repetition)]({{ site.baseurl }}{% link getting-started/recurring-tasks.md %}).

### Callouts in Divs


<div class="code-example" markdown="1">
Warning
{: .label .label-yellow}
Whenever Tasks behaves in an unexpected way, **please try restarting Obsidian**.

---

Warning
{: .label .label-yellow}
Tasks only supports **single-line checklist items**.

The task list rendered through this plugin **and** the checklist items
from which the task list is built render only the first line of the item.
Text after the first line in a multi-line checklist item is
ignored (but is unaffected in the stored `.md` file).

This works:

```markdown
-   [ ] This is a task
    -   This is a sub-item
    -   Another sub-item
    -   [ ] And a sub task
        -   Even more details
```

The following _does not work:_

```markdown
-   [ ] This task starts on this line
        and then its description continues on the next line
```

---

Warning
{: .label .label-yellow}
Tasks can read tasks that are in **numbered lists**.

> [!success] Released
Reading tasks inside numbered lists was introduced in Tasks 1.20.0.

For example:

```markdown
1. [ ] Do first step
2. [ ] Do next step
3. [ ] Do following step
```

Editing and toggling tasks in numbered lists works fine: the original number is preserved.

However, when these tasks are displayed in tasks blocks they are displayed as ordinary bullet list items.

This is because they will usually be displayed in a completely different order than in the original list, often mixed in with tasks from bullet lists. The original numbers in this case just don't make sense.

---

Warning
{: .label .label-yellow}
Tasks can read tasks that are inside **blockquotes** or [Obsidian's built-in callouts](https://help.obsidian.md/How+to/Use+callouts).

> [!success] Released
Reading tasks inside callouts and blockquotes was introduced in Tasks 1.11.1

However, under the following very specific circumstance, Tasks cannot add or remove completion dates or make the next copy of a recurring task:

- Obsidian is in Live Preview editor mode (pencil icon in lower right corner),
- AND the task's markdown is in a callout,
- AND the user clicked on the task's checkbox to complete or re-open the task.

If you toggle a task's status in this situation, you will see a warning. Use the command `Tasks: Toggle Done`, or switch to Reading View (book icon in lower right corner) to click the checkbox.

Completing a task by clicking its checkbox from a `tasks` query block _will_ work in any editor mode, even if the query is inside a callout.

---

Warning
{: .label .label-yellow}

Tasks cannot read tasks that are **inside code blocks**, such as the ones used by the **Admonitions plugin**. Use Obsidian's built-in callouts instead.

---

Warning
{: .label .label-yellow}

Obsidian supports two styles of **comments**:

- `<!-- I am text in a comment -->`
- `%% I am text in a comment %%`

Tasks does read any tasks that are inside these comments, because Obsidian does not read them.

---

Warning
{: .label .label-yellow}
Tasks can only render **inline footnotes**. Regular footnotes are not supported.

```markdown
-   [ ] This is a task^[with a working inline footnote]
-   [ ] This footnote _will not work_[^notworking]
```

---

Warning
{: .label .label-yellow}
Tasks' support for **block quotes inside tasks** is limited. It renders correctly, but since Tasks only supports a single line, the meta-data of the task will be inside the block quote.

---

Warning
{: .label .label-yellow}
Tasks won't render **spaces around list items** if you have a list with empty lines.

```markdown
-   [ ] First task before the empty line

-   [ ] Another task. The empty line above will _not_ result in the tasks being more spaced out.
```

---

Warning
{: .label .label-yellow }

Tasks reads task lines **backwards from the end of the line**, looking for metadata emojis with values, tags and block links. As soon as it finds a value that it does not recognise, it stops reading.

This means that you can only put **block links** (`^link-name`) and **tags** after metadata such as dates, priorities, recurrence rules. Anything else will break the parsing of dates, priorities and recurrence rules.

```markdown
-   [ ] Task with priority placed before tag _priority will be recognized_ 🔼 #tag
-   [ ] Task with date placed before tag _date will be recognized_ 📅 2021-04-09 #tag
-   [ ] Task with date placed before other text _date will be not recognized_ 📅 2021-04-09 other text
-   [ ] Task with block link _works_ 📅 2021-04-09 ^e5bebf
```

If you are concerned that some values in a task are not being parsed as you intended, perhaps because a task is not being found by Tasks searches, you can view the task in the [[getting-started/create-or-edit-task|‘Create or edit Task’ Modal]].

If there are any **Tasks emojis visible in the Description field**, close the modal and delete or move to the left any unrecognised text.

![Create or Edit Modal](../images/modal-showing-unparsed-emoji.png)
<br>The `Tasks: Create or edit` modal showing a due date that was not parsed, due to trailing `other text`.

---

Warning
{: .label .label-yellow}
Tasks only supports checklist items in markdown files with the file extension `.md`.

</div>

---

Important
{: .label .label-yellow }

A recurring task should have a due date. The due date and the recurrence rule must appear after the task's description.

---

Info
{: .label .label-blue }
Headings are displayed in case-sensitive alphabetical order, not the original order.


## Urgency Scores

The scores are as follows:

<table>
<thead>
  <tr>
    <th colspan="2">Property</th>
    <th>Score</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="5">Due</td>
    <td>More than 7 days overdue</td>
    <td><code>12.0</code></td>
  </tr>
  <tr>
    <td rowspan="2">Due between 7 days ago and in 14 days</td>
    <td>Range of <code>12.0</code> to <code>0.2</code></td>
  </tr>
  <tr>
    <td>Example for "today": <code>9.0</code></td>
  </tr>
  <tr>
    <td>More than 14 days until due</td>
    <td><code>0.2</code></td>
  </tr>
  <tr>
    <td>None</td>
    <td><code>0.0</code></td>
  </tr>

  <tr>
    <td rowspan="4">Priority</td>
    <td>High</td>
    <td><code>6.0</code></td>
  </tr>
  <tr>
    <td>Medium</td>
    <td><code>3.9</code></td>
  </tr>
  <tr>
    <td>None</td>
    <td><code>1.95</code></td>
  </tr>
  <tr>
    <td>Low</td>
    <td><code>0.0</code></td>
  </tr>

  <tr>
    <td rowspan="3">Scheduled</td>
    <td>Today or earlier</td>
    <td><code>5.0</code></td>
  </tr>
  <tr>
    <td>Tomorrow or later</td>
    <td><code>0.0</code></td>
  </tr>
  <tr>
    <td>None</td>
    <td><code>0.0</code></td>
  </tr>

  <tr>
    <td rowspan="3">Starts</td>
    <td>Today or earlier</td>
    <td><code>0.0</code></td>
  </tr>
  <tr>
    <td>Tomorrow or later</td>
    <td><code>-3.0</code></td>
  </tr>
  <tr>
    <td>None</td>
    <td><code>0.0</code></td>
  </tr>
</tbody>
</table>

# Quick Reference

[1]: https://obsidian-tasks-group.github.io/obsidian-tasks/queries/filters/
[2]: https://obsidian-tasks-group.github.io/obsidian-tasks/queries/sorting/
[3]: https://obsidian-tasks-group.github.io/obsidian-tasks/queries/grouping/
[4]: https://obsidian-tasks-group.github.io/obsidian-tasks/queries/layout/
[5]: https://obsidian-tasks-group.github.io/obsidian-tasks/queries/combining-filters/

This table summarizes the filters and other options available inside a `tasks` block.
