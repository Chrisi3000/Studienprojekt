# Samplot – Technical Documentation of Insertion Support

## Introduction

Insertions were previously not supported because the inserted sequence is absent from the reference genome, making it difficult to represent with standard read-alignment visualizations. 

The objective is to detect and visualize insertions. 

Support for insertion detection and visualization was added.

## 1. General Changes

### 1.1 Extension of Read Types and Color Definitions

**Added Code:**
```python
"Insertion": "purple",
"Missing mate paired-end read 1": "magenta",
"Missing mate paired-end read 2": "cyan"
```

```python
READ_TYPES_USED = {
    "Deletion/Normal": False,
    "Duplication": False,
    "Inversion": False,
    "Insertion": False,
    "Aligned long read": False,
    "Linked read": False,
    "Split-read": False,
    "Paired-end read": False,
    "Missing mate paired-end read": False
}
```

**Explanation:**

The color definitions were extended to support insertion visualization. Insertions in long reads are displayed in purple, while magenta and cyan are used to distinguish paired-end reads based on the direction of their missing mate.

The `READ_TYPES_USED` dictionary was extended to track whether insertions or paired-end reads with missing mates are present in the visualization. This allows the corresponding legend entries to be displayed only when needed.

---

### 1.2 Custom Legend Handles

**Added Code:**
```python
class TwoColorLine:
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2

class TwoColorLineHandler(HandlerBase):
    def create_artists(
        self, legend, orig_handle, xdescent, ydescent,
        width, height, fontsize, trans
    ):
        y = ydescent + height/2
        x_mid = xdescent + width/2

        left = Line2D(
            [xdescent, x_mid], [y, y],
            color=orig_handle.color1,
            linewidth=1.5,
            transform=trans
        )

        right = Line2D(
            [x_mid, xdescent+width], [y, y],
            color=orig_handle.color2,
            linewidth=1.5,
            transform=trans
        )

        return [left, right]
```

**Explanation:**

The `TwoColorLine` and `TwoColorLineHandler` classes were
introduced to represent paired-end reads with unmapped mates
in the legend.

Two horizontal line segments with different colors are combined
into a single legend symbol. This allows both orientations
(magenta and cyan) to be represented by one legend entry.

**Added Code:**
```python
class InsertionHandle:
    pass

class InsertionHandler(HandlerBase):
    event_type: Final = "Insertion"

    def create_artists(
        self, legend, orig_handle, xdescent, ydescent,
        width, height, fontsize, trans
    ):
        x = width / 2

        line = Line2D(
            [x, x],
            [height * 1.5, height * 0.5],
            color=COLORS[InsertionHandler.event_type],
            lw=1,
            transform=trans
        )

        triangle = Line2D(
            [x],
            [height * 0.2],
            marker="v",
            color=COLORS[InsertionHandler.event_type],
            markerfacecolor=COLORS[InsertionHandler.event_type],
            linestyle="None",
            markersize=3,
            transform=trans
        )

        return [line, triangle]
```

**Explanation:**

The `InsertionHandle` and `InsertionHandler` classes were
introduced to create a custom legend symbol for insertions
in long reads.

The symbol consists of a vertical purple line and a
downward-pointing triangle, matching the graphical
representation of insertions in the long read visualization.

Both custom handlers ensure that the legend is consistent
with the newly introduced visualization elements.

---

### 1.3 Integration of Custom Legend Entries

**Function:** `plot_legend()`

**Added Code:**
```python
"Insertion": "purple",
"Missing mate paired-end read 1": "magenta",
"Missing mate paired-end read 2": "cyan"
```

**Modified Code:**
```python
for read_type in READ_TYPES_USED:
    if read_type in read_colors and read_type != "Insertion":
```

**Explanation:**

The color dictionary was extended to include the newly introduced
visualization elements. The insertion event is excluded from the
standard legend generation because it requires a custom symbol.

**Added Code:**
```python
if READ_TYPES_USED["Insertion"]:
    marker_labels.append("Insertion")
    insertion_handle = InsertionHandle()
    legend_elements.append(insertion_handle)

if READ_TYPES_USED["Missing mate paired-end read"]:
    marker_labels.append("Missing mate paired-end read")

    legend_elements.append(
        TwoColorLine(read_colors["Missing mate paired-end read 1"],
                     read_colors["Missing mate paired-end read 2"])
    )
```

**Explanation:**

The custom legend entries for long read insertions and paired-end
reads with unmapped mates are added based on their corresponding
flags in `READ_TYPES_USED`.

This ensures that the entries are only displayed if the
corresponding visualization elements are present in the plot.

**Modified Code:**
```python
fig.legend(
    legend_elements, marker_labels, loc=1,
    fontsize=legend_fontsize, frameon=False,
    handler_map={
        InsertionHandle: InsertionHandler(),
        TwoColorLine: TwoColorLineHandler(),
    }
)
```

**Explanation:**

The `handler_map` parameter was added to associate the custom
legend handles with their corresponding handlers introduced
in Section 1.2.

This integrates the new symbols into the existing Samplot legend
without changing the representation of other read or event types.

## 2. Long Reads

### 2.1 Insertion Length Threshold

**Added Code:**
```python
INSERTION_LENGTH = 50
```

**Explanation:**

The `INSERTION_LENGTH` parameter defines the length threshold in base pairs (bp) above which insertions are detected and visualized in long reads. The default threshold is set to 50 bp, meaning that only insertions larger than 50 bp are considered.

---

### 2.2 Extension of the Alignment Class

**Class:** `Alignment`

**Modified Code:**
```python
def __init__(self, chrm, start, end, strand, query_position, insertion_size=0):
```

**Added Code:**
```python
self.insertion_size = insertion_size
```

**Explanation:**

The `Alignment` class was extended with the `insertion_size`
parameter to store the length of an insertion in base pairs (bp).

This makes the insertion length available during further processing
and visualization of long read alignments.

The default value is set to `0` for alignments without an associated
insertion, maintaining compatibility with the existing implementation.

---

### 2.3 Detection of Insertions from CIGAR Strings

**Function:** `get_alignments_from_cigar()`

**Modified Code:**
```python
elif op == CIGAR_MAP["I"]:
    if length > INSERTION_LENGTH:
        alignments.append(
            Alignment(chrm, curr_pos, curr_pos, strand, q_pos, length)
        )
    q_pos += length
```

**Explanation:**

The processing of CIGAR strings was extended to explicitly handle
insertion operations (`I`). If the insertion length exceeds the
defined `INSERTION_LENGTH` threshold, a separate `Alignment`
instance is created containing the insertion position and length.

Since the inserted sequence is not present in the reference genome,
the start and end positions are identical.

Only the query position (`q_pos`) is advanced by the insertion
length, while the reference position (`curr_pos`) remains unchanged.

This allows insertions to be stored and accessed during subsequent
processing and visualization of long reads.

---

### 2.4 Preservation of Insertions during Alignment Merging

**Function:** `merge_alignments()`

**Modified Code:**
```python
if alignment.pos.start == alignment.pos.end:
    merged_alignments.append(alignment)
elif (
    alignment.pos.chrm == merged_alignments[-1].pos.chrm
    and alignment.pos.start < merged_alignments[-1].pos.end + min_gap
    and merged_alignments[-1].pos.start != merged_alignments[-1].pos.end
):
    merged_alignments[-1].pos.end = alignment.pos.end
else:
    merged_alignments.append(alignment)
```

**Explanation:**

Previously, adjacent alignments within the defined `min_gap`
distance were merged without considering insertions.

Since insertions are represented by alignments with identical
start and end positions, two additional conditions were introduced:

- Insertion alignments are added separately instead of being
  merged with the preceding alignment.
- Subsequent alignments cannot be merged into an insertion alignment.

This ensures that insertions remain separate alignment objects
and that their position and length are preserved for visualization.
The merging behavior for regular adjacent alignments remains unchanged.

---

### 2.5 Integration of Insertions into the Long Read Plotting Plan

**Function:** `get_long_read_plan()`

**Added Code:**
```python
if curr.insertion_size > INSERTION_LENGTH:
    start = genome_interval(curr.pos.chrm, curr.pos.start, curr.pos.start + curr.insertion_size)
    end = genome_interval(curr.pos.chrm, curr.pos.start, curr.pos.start + curr.insertion_size)
    info = {"TYPE": "Insertion", "LENGTH": curr.insertion_size}
    steps.append(plan_step(start, end, "LONGREAD", info=info))
    add_align_step(curr, steps, ranges)
```

**Explanation:**

The event classification was extended to recognize insertions
as a separate event type within the long read plotting plan.

If the insertion size exceeds the defined threshold, a new
plotting step is created. The event type `Insertion` and the
insertion length are stored in the `info` dictionary.

The plotting interval is defined using the insertion position
and length. This interval is an artificial representation for
visualization purposes, since the inserted sequence does not
occupy any positions in the reference genome.

This allows insertions to be distinguished from other structural
variants and visualized separately during the plotting process.

---

### 2.6 Read Support-Based Line Width and Color

**Added Code:**
```python
def support_to_linewidth(n_reads):
    if n_reads > 10:
        return 2.0
    elif n_reads > 5:
        return 1.6
    elif n_reads > 1:
        return 1.2
    return 0.8

def support_to_color(n_reads):
    if n_reads > 10:
        level = 0.99
    elif n_reads > 5:
        level = 0.90
    elif n_reads > 1:
        level = 0.80
    else:
        level = 0.70
    return plt.cm.Purples(level)
```

**Explanation:**

Two helper functions were introduced to adjust the line width
and color intensity of insertion markers based on the number
of supporting reads.

Insertions supported by more reads are represented by thicker
lines and darker shades of purple, making their read support
visually distinguishable.

| Supporting Reads | Line Width | Color Intensity |
|------------------|------------|-----------------|
| 1                | 0.8        | 0.70            |
| 2–5              | 1.2        | 0.80            |
| 6–10             | 1.6        | 0.90            |
| >10              | 2.0        | 0.99            |

---

### 2.7 Visualization of Long Read Insertions

**Modified Function Signature:**
```python
def plot_long_reads(long_reads, ax, ranges, curr_min_insert_size,
                    curr_max_insert_size, limitInsertion,
                    jitter_bounds, yaxis_label_fontsize):
```

**Added Code:**
```python
"Insertion": "purple"
```

```python
ax2 = ax.twinx()
insertion_clusters = {}
```

**Added Event Handling:**
```python
elif event_type == "Insertion":
    range_hit = get_range_hit(ranges, step.start_pos.chrm,
                              step.start_pos.start)
    range_width = 1.0 / len(ranges)

    insertion_length = step.info["LENGTH"]
    x = p[0]
    y_upper = insertion_length + insertion_length

    height = max_gap * 1.15 if max_gap > 0 else 10
    curr_max_insert_size = max(curr_max_insert_size, height)

    chrm = step.start_pos.chrm
    pos = step.start_pos.start

    key = (chrm, pos)
    cluster = insertion_clusters.get(key)

    if cluster is None:
        size = support_to_linewidth(1)
        line, = ax2.plot(
            [x, x], [insertion_length, y_upper],
            marker=7, markevery=[0],
            c=support_to_color(1),
            markersize=size + 3, lw=size
        )
        insertion_clusters[key] = {
            "reads": {read_name},
            "line": line,
            "x": x,
            "y_upper": y_upper
        }
    else:
        cluster["reads"].add(read_name)
        n_reads = len(cluster["reads"])
        size = support_to_linewidth(support_to_linewidth(n_reads))
        cluster["line"].set_linewidth(size)
        cluster["line"].set_markersize(size + 3)
        cluster["line"].set_color(support_to_color(n_reads))

    limitInsertion = max(limitInsertion, insertion_length)
```

**Explanation:**

Insertions are visualized as vertical purple lines at their
genomic breakpoint. A downward-pointing marker indicates the
insertion length on the additional y-axis.

The `insertion_clusters` dictionary groups insertions occurring
at exactly the same genomic position on the same chromosome.

Instead of drawing overlapping markers for each supporting read,
the existing marker is updated based on the number of unique
supporting reads. Its line width, marker size and color intensity
are adjusted accordingly.

The maximum insertion length is tracked using `limitInsertion`
to determine the required range of the additional y-axis.

**Additional Y-Axis Configuration:**
```python
ax2.set_ylim([0, max(1, limitInsertion * 2.1)])
ax2.spines["top"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["left"].set_visible(False)

if limitInsertion > 0:
    ax2.tick_params(axis="y", colors="grey",
                    labelsize=yaxis_label_fontsize)
    ax2.spines["right"].set_position(("outward", 30))
    ax2.spines["right"].set_color("grey")
else:
    ax2.tick_params(axis="y", which="both",
                   left=False, right=False,
                   labelleft=False, labelright=False)
    ax2.spines["right"].set_visible(False)
```

**Explanation:**

A secondary y-axis was introduced to display insertion lengths
independently of the existing long read visualization.

The axis is dynamically scaled according to the largest insertion
and is only visible if insertions are present in the plotted region.

---

### 2.8 Integration of Insertion Visualization into Sample Plotting

**Function:** `plot_samples()`

**Added Code:**
```python
limitInsertion = 0
```

**Modified Code:**
```python
elif len(curr_long_reads) > 0:
    curr_min_insert_size, curr_max_insert_size = plot_long_reads(
        curr_long_reads,
        curr_ax,
        ranges,
        curr_min_insert_size,
        curr_max_insert_size,
        limitInsertion,
        jitter_bounds,
        yaxis_label_fontsize
    )
```

**Explanation:**

The variable `limitInsertion` is initialized separately for each
haplotype and passed to `plot_long_reads()` to track the maximum
insertion length and determine the scale of the additional y-axis.

The `yaxis_label_fontsize` parameter is also passed to maintain
consistent formatting with the existing axes.

**Added Code:**
```python
has_long_reads = any(
    len(read_data["all_long_reads"][i].get(hp, {})) > 0
    for hp in hps
)

if has_long_reads:
    insert_ax = curr_ax.twinx()
    insert_ax.spines["right"].set_position(("outward", 40))
    insert_ax.spines["top"].set_visible(False)
    insert_ax.spines["bottom"].set_visible(False)
    insert_ax.spines["left"].set_visible(False)
    insert_ax.spines["right"].set_visible(False)
    insert_ax.tick_params(
        axis="y",
        right=False,
        labelright=False,
        length=0
    )
    insert_ax.set_ylabel("Insertion Length", fontsize=8, labelpad=10)
```

**Explanation:**

An additional axis is created to display the "Insertion Length"
label. Its spines and ticks are hidden because the actual
insertion length scale is already generated in `plot_long_reads()`.

The label is only added to samples containing long reads.

---



---


## 3. Paired-End Reads

### 3.1 Counting Reads with Unmapped Mates

**Added Code:**
```python
def add_unmapped_mate_interval(read, counts, offset, range_end):
    """Adds the mapped interval of a read whose mate is unmapped."""
    if (
        read.is_unmapped
        or not read.is_paired
        or read.is_secondary
        or read.is_supplementary
        or not read.mate_is_unmapped
    ):
        return

    start = max(read.reference_start, offset)
    end = min(read.reference_end, range_end)
    if start < end:
        strand_column = 1 if read.is_reverse else 0
        counts[start - offset:end - offset, strand_column] += 1
```

**Explanation:**

This function identifies primary mapped paired-end reads whose mates are unmapped and counts their coverage within the displayed genomic region.

The alignment interval is restricted to the boundaries of the region. Forward and reverse reads are counted separately in two columns of the `counts` array, allowing the direction of missing mates to be distinguished in the visualization.

---

### 3.2 Visualization of Unmapped Mate Coverage

**Added Code:**
```python
def plot_unmapped_mate_bars(counts, ax, ranges, yaxis_label_fontsize):
    """Plots mapped intervals whose paired mate is unmapped."""
    bar_x = {0: [], 1: []}
    bar_y = {0: [], 1: []}
    bar_width = {0: [], 1: []}

    for range_index, r in enumerate(ranges):
        region_len = r.end - r.start
        if region_len <= 0:
            continue
        scale = 1.0 / len(ranges)
        width = scale / region_len
        for position in range(r.start, r.end):
            values = counts.get(r.chrm, {}).get(position, (0, 0))
            for strand_column in (0, 1):
                value = values[strand_column]
                if value:
                    bar_x[strand_column].append(
                        scale * range_index + scale * (position - r.start) / region_len
                    )
                    bar_y[strand_column].append(value)
                    bar_width[strand_column].append(width)

    max_bar_height = max((max(values) for values in bar_y.values() if values), default=0)
    if max_bar_height == 0:
        return None

    bar_ax = ax.twinx()
    bar_ax.spines["right"].set_position(("outward", 40))
    bar_ax.spines["right"].set_color("grey")
    bar_ax.spines["top"].set_visible(False)
    bar_ax.spines["bottom"].set_visible(False)
    bar_ax.spines["left"].set_visible(False)
    bar_ax.spines["right"].set_visible(True)
    bar_ax.tick_params(axis="y", colors="grey", labelsize=yaxis_label_fontsize)
    bar_ax.set_ylabel("Unmapped Read Count", fontsize=8, labelpad=10)
    step = max(1, max_bar_height // 10)
    bar_ax.set_yticks(range(0, max_bar_height + 1, step))

    for strand_column, color in ((0, COLORS["Missing mate paired-end read 1"]),
                                 (1, COLORS["Missing mate paired-end read 2"])):
        bar_ax.bar(
            bar_x[strand_column],
            bar_y[strand_column],
            width=bar_width[strand_column],
            align="edge",
            color=color,
            alpha=0.35,
            linewidth=0,
        )
    return bar_ax
```

**Explanation:**

This function visualizes the previously collected counts of mapped
paired-end reads with unmapped mates as a bar plot.

The genomic positions are scaled to match the existing Samplot
coordinate system. Forward and reverse reads are plotted separately
in magenta and cyan using semi-transparent bars.

An additional y-axis is created on the right side of the plot to
display the read counts independently of the existing visualization.
The axis is only added if reads with unmapped mates are present.

This makes regions with an increased number of missing mates more
visible and helps identify potential insertion breakpoints.

---

### 3.3 Extension of the Read Constructor

**Class:** `PairedEnd`

**Modified Code:**
```python
def __init__(self, chrm, start, end, is_reverse, MI_tag, HP_tag, mate_is_unmapped=False):
```

**Added Code (init):**
```python
self.mate_is_unmapped = mate_is_unmapped
```

**Explanation:**

The constructor was extended with the `mate_is_unmapped` parameter to store whether the corresponding mate of a paired-end read is unmapped. This information is stored as an instance attribute and can be accessed during further processing and visualization.

The default value is set to `False` to maintain compatibility with the existing implementation.

---

### 3.4 Passing Unmapped Mate Information

**Function:** `add_pair_end()`

**Modified Code:**
```python
pe = PairedEnd(
    bam_file.get_reference_name(read.reference_id),
    read.reference_start,
    read.reference_end,
    read.is_reverse,
    MI_tag,
    HP_tag,
    read.mate_is_unmapped
)
```

**Explanation:**

The creation of the `PairedEnd` instance was extended to pass the
`mate_is_unmapped` flag from the original Pysam read.

This ensures that information about unmapped mates is preserved when
converting Pysam reads into Samplot's internal `PairedEnd` objects
and remains available for further processing and visualization.

---

### 3.5 Preservation of Reads with Unmapped Mates during Downsampling

**Function:** `sample_normal()`

**Modified Code:**
```python
for read_name in pairs:
    pair = pairs[read_name]
    if len(pair) != 2:
        if pair[0].mate_is_unmapped:
            sampled_pairs[read_name] = pair

        continue
```

**Explanation:**

Previously, incomplete read pairs were excluded during downsampling.
The function was modified to retain reads whose mates are explicitly
marked as unmapped.

This prevents the loss of potential insertion signals during
downsampling, while other incomplete read pairs are still excluded.

---

### 3.6 Extension of the Paired-End Plotting Plan

**Modified Code:**
```python
def get_pair_plan(ranges, pair, linked_plan=False):
    if pair is None:
        return None

    first = pair[0]
    mate_missing = len(pair) != 2 and first.mate_is_unmapped

    if not mate_missing:
        second = pair[1]

        # see if they are part of a linked read
        if not linked_plan and (first.MI or second.MI):
            return None

        second_hit = get_read_hit(ranges, second)
        if second_hit is None:
            return None

    first_hit = get_read_hit(ranges, first)
    if first_hit is None:
        return None

    start = genome_interval(
        first.pos.chrm,
        max(first.pos.start, ranges[first_hit].start),
        max(first.pos.start, ranges[first_hit].start),
    )

    if not mate_missing:
        insert_size = get_pair_insert_size(ranges, pair)

        end = genome_interval(
            second.pos.chrm,
            min(second.pos.end, ranges[second_hit].end),
            min(second.pos.end, ranges[second_hit].end),
        )
    else:
        insert_size = 2000

        end = genome_interval(
            first.pos.chrm,
            min(first.pos.end, ranges[first_hit].end),
            min(first.pos.end, ranges[first_hit].end),
        )

    step = plan_step(start, end, "PAIREND")

    step.info = {"TYPE": get_pair_event_type(pair),
                 "INSERTSIZE": insert_size}

    if mate_missing:
        step.info["MATE_IS_UNMAPPED"] = first.strand

    return insert_size, step
```

**Explanation:**

The function was extended to generate plotting plans for paired-end
reads with an unmapped mate.

For complete read pairs, the existing processing remains unchanged.
If the mate is unmapped, the start and end positions of the mapped
read are used to define the plotting interval.

Since the actual insert size cannot be calculated without the mate,
a fixed placeholder value of 2000 bp is assigned for plotting purposes.

Additionally, the strand orientation of the mapped read is stored
in `MATE_IS_UNMAPPED` within the plotting plan. This information is
used to determine the direction, color and orientation of the marker
during visualization.

---

### 3.7 Checking Read Positions within the Plotting Region

**Added Code:**
```python
def get_read_hit(ranges, read):
    """Make sure both ends are in the plotted region
    """
    s_hit = get_range_hit(ranges, read.pos.chrm, read.pos.start)
    e_hit = get_range_hit(ranges, read.pos.chrm, read.pos.end)
    if s_hit is None and e_hit is None:
        return None

    return e_hit if e_hit is not None else s_hit
```

**Explanation:**

This function checks whether the start or end position of an
individual read is within the plotted genomic region.

If neither position is within the region, the function returns
`None`. Otherwise, it returns the corresponding range index,
prioritizing the end position.

This allows the position of a mapped read to be evaluated
independently of its mate and avoids duplicate code in
`get_pair_plan()`.

---

### 3.8 Extension of Paired-End Event Classification

**Function:** `get_pair_event_type()`

**Modified Code:**
```python
# Case Mate unmapped (read either forward or reverse strand)
if len(pe_read) != 2 and pe_read[0].mate_is_unmapped:
    # first strand is True (forward) - our read could be forward or reverse
    first_strand = pe_read[0].strand if pe_read[0].strand else not pe_read[0].strand
    event_type = event_by_strand[first_strand, not first_strand]
else:
    event_type = event_by_strand[pe_read[0].strand, pe_read[1].strand]

return event_type
```

**Explanation:**

The event classification was extended to handle paired-end reads
with an unmapped mate.

Since the strand orientation of the missing mate is unavailable,
a conventional forward-reverse orientation is assumed, resulting
in the event type `Deletion/Normal`.

This prevents errors when accessing the missing second read and
maintains compatibility with the existing event classification.
Complete read pairs are classified as before.

---

### 3.9 Visualization of Paired-End Reads with Unmapped Mates

**Modified Function Signature:**
```python
def plot_pair_plan(ranges, step, ax, marker_size, jitter_bounds, stepSize=None):
```

**Added Code:**
```python
if stepSize is not None:
    y = stepSize
```

```python
x_start = p[0]
x_end = p[1]

if "MATE_IS_UNMAPPED" in step.info:
    READ_TYPES_USED["Missing mate paired-end read"] = True
    if step.info["MATE_IS_UNMAPPED"] == True:
        ax.plot(
            [x_start, x_end],
            [y, y],
            "-",
            color=COLORS["Missing mate paired-end read 1"],
            alpha=1,
            lw=1.0,
            marker="|",
            markersize=marker_size,
            markevery=[0],
            zorder=10,
        )
    else:
        ax.plot(
            [x_start, x_end],
            [y, y],
            "-",
            color=COLORS["Missing mate paired-end read 2"],
            alpha=1,
            lw=1.0,
            marker="|",
            markersize=marker_size,
            markevery=[1],
            zorder=10,
        )

    return True
```

**Explanation:**

The plotting function was extended to visualize paired-end reads
with an unmapped mate separately from complete read pairs.

Depending on the strand orientation of the mapped read, different
colors (magenta and cyan) and marker positions are used. A vertical
marker is placed at one end of the horizontal line to indicate the
orientation of the read and the direction of its missing mate.

The optional `stepSize` parameter allows the y-position to be
specified explicitly instead of using the insert size with jitter.
This enables the stair-step layout and prevents overlapping reads.

Furthermore, `READ_TYPES_USED` is updated to include the corresponding
legend entry. The visualization of complete read pairs remains unchanged.

---

### 3.10 Implementation of the Stair-Step Layout

**Function:** `plot_pairs()`

**Added Code:**
```python
steps.sort(key=lambda step: step.start_pos.start)
stairStep = 0

axRange = ranges[0]
axSize = axRange.end - axRange.start

n_steps_pe = 0
for step in steps:
    if "MATE_IS_UNMAPPED" in step.info:
        n_steps_pe += 1

if n_steps_pe > 1:
    stepHeight = max_event / (n_steps_pe - 1)
else:
    stepHeight = 0
```

**Modified Code:**
```python
for step in steps:
    if "MATE_IS_UNMAPPED" in step.info:
        if plot_pair_plan(ranges, step, ax, marker_size, jitter_bounds,
                          stepSize=stairStep * stepHeight):
            stairStep += 1
    else:
        plot_pair_plan(ranges, step, ax, marker_size, jitter_bounds)
```

**Explanation:**

The plotting steps are sorted according to their genomic start
position to keep spatially adjacent reads close together.

The number of reads with unmapped mates is determined and used
to calculate a uniform vertical spacing (`stepHeight`) based on
the maximum event size.

Each successfully plotted read with an unmapped mate is assigned
an increasing y-position, resulting in a stair-step layout.
This reduces overlapping reads and makes clusters of reads with
missing mates easier to identify.

Complete read pairs are still plotted using the original
insert-size-based visualization.

---

### 3.11 Collection and Storage of Unmapped Mate Counts

**Function:** `get_read_data()`

**Added Code:**
```python
all_unmapped_mate_counts = []
```

```python
unmapped_mate_counts = {hp: {} for hp in haplotypes}
```

```python
range_unmapped_mate_counts = {
    hp: np.zeros((range_len, 2), dtype=int) for hp in haplotypes
}
```

**Explanation:**

Additional data structures were introduced to store the coverage
of reads with unmapped mates separately for each BAM file,
haplotype and genomic region.

The two columns of the NumPy array represent forward and reverse
reads, respectively.

**Added Code within Short Read Processing:**
```python
hp = 0 if ignore_hp or not read.has_tag("HP") else read.get_tag("HP")
add_unmapped_mate_interval(
    read,
    range_unmapped_mate_counts[hp],
    range_start,
    range_end,
)
```

**Explanation:**

During short read processing, the previously introduced
`add_unmapped_mate_interval()` function is called to collect
the coverage of mapped reads with unmapped mates for the
corresponding haplotype.

**Added Code within Coverage Processing:**
```python
if range_unmapped_mate_counts[hp].sum() > 0:
    unmapped_mate_counts[hp].setdefault(chrm, {})
    for position in range(range_start, range_end):
        values = range_unmapped_mate_counts[hp][position - range_start]
        if values.any():
            unmapped_mate_counts[hp][chrm][position] = [
                int(values[0]),
                int(values[1]),
            ]
```

**Explanation:**

The collected counts are transferred from the NumPy arrays
into a nested dictionary organized by haplotype, chromosome
and genomic position.

Only positions with non-zero counts are stored to reduce
memory usage.

**Added Code:**
```python
all_unmapped_mate_counts.append(unmapped_mate_counts)
```

**Extension of the `read_data` Dictionary:**
```python
"all_unmapped_mate_counts": all_unmapped_mate_counts,
```

**Explanation:**

The collected counts are stored for each BAM file and included
in the returned `read_data` dictionary.

Since the counts are collected before downsampling, they represent
all qualifying reads rather than only the sampled reads.

This makes the strand-specific coverage of reads with unmapped
mates available for the subsequent bar plot visualization.

---

### 3.12 Integration of Unmapped Mate Coverage into Sample Plotting

**Function:** `plot_samples()`

**Added Code:**
```python
curr_unmapped_mate_counts = {}
if hp in read_data["all_unmapped_mate_counts"][i]:
    curr_unmapped_mate_counts = read_data["all_unmapped_mate_counts"][i][hp]
```

**Explanation:**

The previously collected unmapped mate counts are retrieved
from the `read_data` dictionary for the corresponding sample
and haplotype.

**Added Code:**
```python
plot_unmapped_mate_bars(
    curr_unmapped_mate_counts,
    curr_ax,
    ranges,
    yaxis_label_fontsize,
)
```

**Explanation:**

The retrieved counts are passed to `plot_unmapped_mate_bars()`
to integrate the strand-specific coverage of reads with unmapped
mates into the existing sample plot.

The function handles the creation and scaling of the additional
y-axis independently and only generates the bar plot if
corresponding reads are present.