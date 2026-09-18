**本仓库并非上游官方仓库，仅为 Kaishi 1.5k 的简体中文本地化衍生版本；如发现数据错误，请先分清是「上游客观数据问题」还是「中文翻译问题」，再到对应仓库反馈。**

# Kaishi 1.5k zh-CN

面向中文母语者的日语入门 Anki 卡组，本地化自上游 [donkuri/Kaishi](https://github.com/donkuri/Kaishi)。当前数据基线 **v2.4.3**，zh-CN 本地化版本 **v1.3.0.1**。

> [!NOTE]
> **关于本页结构：** 从页首到「zh-CN 版本比上游多了什么」为止，是 zh-CN 本地化说明，**非上游原版 README 内容**；自下方「以下是英文原版牌组的 README.md 的翻译」起，是对上游 [UPSTREAM_README.md](./UPSTREAM_README.md) 的忠实翻译。翻译正文中凡标注 **⚠️ 非上游原版内容** 的部分，同为 zh-CN 本地化补充。

## 项目关系

| 类型        | 仓库                                                                            | 版本         | 说明                                   |
| --------- | ----------------------------------------------------------------------------- | ---------- | ------------------------------------ |
| 上游        | [donkuri/Kaishi](https://github.com/donkuri/Kaishi)                           | v2.4.3     | 客观数据来源（音高重音、例句、配图、音频、词汇注释）           |
| zh-CN 老仓库 | [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn)               | v1.3.0     | 早期（v2.2.7）中文本地化仓库，提供中文释义、词性、活用形的基础翻译 |
| 本仓库       | [Angle-AOB/kaishi-1.5k-zh-cn](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn) | v1.3.0.1 起 | 从老仓库派生，提供后续 zh-CN 本地化迭代与上游同步         |
| 更新日志      | [CHANGELOG.md](./CHANGELOG.md)                                                | —          | 每次发布的详细变更（同步了哪些上游数据、翻译了哪些新增注释、升级路径等） |

**双版本号约定：** CHANGELOG 里标题形如 ` v1.3.0.1（上游版本 v2.4.3）`——前者是 zh-CN 本地化版本，延续老仓库 v1.x 体系；后者是数据同步基线，与上游 v2.x 对齐。两条版本线并行，不合并、不同步。

## zh-CN 版本比上游多了什么？

本仓库在完整继承上游客观数据的前提下，为中文母语者增加了以下内容：

| 字段                   | 上游原版   | 本仓库 zh-CN 版                           |
| -------------------- | ------ | ------------------------------------- |
| `Word Meaning`       | 英文释义   | **中文释义**（保留老仓库翻译，部分调整）                |
| `Sentence Meaning`   | 英文翻译   | **中文翻译**                              |
| `Notes`              | 英文注释   | **中文注释**（上游新增注释同步翻译）                  |
| `Pitch Accent Notes` | 英文音高说明 | **中文音高说明**（含鼻浊音、音高变化等语言现象的详细解释）       |
| `Pos`（Field 14）      | 无      | **中文词性标注**（zh-CN 独有字段）                |
| `Katsuyou`（Field 15） | 无      | **中文活用形说明**（zh-CN 独有字段，标注动词/形容词的活用类型） |

上游的音高重音数据（`Pitch Accent`）、例句（`Sentence`、`Sentence Furigana`）、图片（`Picture`）、音频（`Word Audio`、`Sentence Audio`）等客观字段与上游 v2.4.3 完全一致，未做本地化改写。

> [!NOTE]
> **注意：** 卡片模板（Front/Back/CSS）默认与上游一致，`Pos` 与 `Katsuyou` 字段虽然存在，但不会自动显示在卡片上。如需展示，请自行在 Back Template 里加入 `{{Pos}}`、`{{Katsuyou}}`。

---

以下是英文原版牌组的 README.md 的翻译：

---

**凡本页未提及的其他牌组，均与本人无任何关联，包括任何 AI 生成或付费修改的版本。**

# Kaishi 1.5k

欢迎访问 **Kaishi 1.5k** 的公开代码仓库。这是一款现代化的 Anki 牌组，旨在帮助初学者入门基础日语词汇。Kaishi 1.5k 采用高度模块化设计，本页面将为你详细介绍各种自定义选项，让你可以随心所欲地调整牌组。牌组正面效果如下：

<img src="https://github.com/donkuri/Kaishi/blob/main/pics/kaishi-front.png" alt="Kaishi 1.5k 卡片正面" style="width: 100%; height: auto">

如你所见，卡片正面同时显示单词和例句，并且单词在句子中被高亮显示，方便你迅速抓住核心信息。当你对单词足够熟悉后，复习效率会更高，因为单词总会最先映入眼帘。默认牌组的背面如下：

<img src="https://github.com/donkuri/Kaishi/blob/main/pics/kaishi-back.png" alt="Kaishi 1.5k 卡片背面" style="width: 100%; height: auto">

与大多数「核心词汇」（Core）类牌组不同，本牌组的振假名（furigana）直接标注了单词读音，其正下方就是词义。接着，你还可以收听单词和例句的音频。如果你需要，也可以添加音高重音（详见下文）。如果某张卡片有相关笔记，笔记会显示在最下方。

[如果你是日语初学者或刚接触沉浸式学习法，请先阅读本指南。](https://donkuri.github.io/learn-japanese/guide/)

### 目录

- [我在哪里获取牌组？](#我在哪里获取牌组)
- [如何使用本牌组？](#如何使用本牌组)
- [其他相关牌组](#其他相关牌组)
- [牌组有哪些自定义选项？](#牌组有哪些自定义选项)
  - [音高重音](#音高重音)
  - [其他次要选项](#其他次要选项)
  - [进阶：自制中→日反向卡片（zh-CN 补充）](#进阶自制中日反向卡片zh-cn-补充)
- [我不想让例句一直显示！](#我不想让例句一直显示)
- [某个词的音频听起来不对！](#某个词的音频听起来不对)
- [如何将 Kaishi 导入到现有牌组之上？](#如何将-kaishi-导入到现有牌组之上)
- [我不喜欢这些图片！](#我不喜欢这些图片)
- [牌组的诞生故事](#牌组的诞生故事)
- [学完本牌组后该做什么？](#学完本牌组后该做什么)
- [牌组的多语言翻译](#牌组的多语言翻译)
- [从老版本 zh-CN 升级到本仓库版本（zh-CN 补充）](#从老版本-zh-cn-升级到本仓库版本zh-cn-补充)
- [致谢](#致谢)
- [反馈与贡献（zh-CN 补充）](#反馈与贡献zh-cn-补充)

## 我在哪里获取牌组？

你可以在本 GitHub 项目的 [releases](https://github.com/donkuri/Kaishi/releases/) 页面下载，或者在 [AnkiWeb](https://ankiweb.net/shared/info/1196762551) 上获取（前提是牌组未处于审核状态）。**本牌组支持 Anki 2.1.50 及以上版本。**

> [!NOTE]
> **⚠️ 非上游原版内容（zh-CN 下载渠道）：**
> 
> - **本仓库（zh-CN 最新版）：** [Releases 页面](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn/releases) 下载 `Kaishi_15k_zh-CN_updated.apkg`
> - **老仓库（zh-CN v1.3.0）：** <https://github.com/maimemo/kaishi-zh-cn>
> 
> 导入方法：Anki → **文件 → 导入** → 选择 `.apkg`。若之前已经装过老版本 zh-CN，请参考本文末尾的[升级章节](#从老版本-zh-cn-升级到本仓库版本zh-cn-补充)。

## 如何使用本牌组？

若想了解 Kaishi 如何融入更宏观的日语学习计划，请参阅[这份指南](https://donkuri.github.io/learn-japanese/guide/)。

## 其他相关牌组

ねむい 基于 Kaishi 1.5k 制作了一款部首牌组。它将 Kaishi 1.5k 中出现的每一个汉字部首，都与牌组中首个包含该部首的单词关联起来，同时还额外收录了一些 Kaishi 本身未包含的部首。**如果你觉得汉字很难，可以将这款部首牌组与 Kaishi 配合使用**，因为它会随着你的学习进度同步介绍汉字部首，助你更高效地拆解汉字。你可以在 [AnkiWeb 上找到它](https://ankiweb.net/shared/info/1722008986)。非常感谢 ねむい！

## 牌组有哪些自定义选项？

你可以通过多种选项来修改卡片。操作方法是：选中 Kaishi 牌组，点击「浏览」（Browse），在牌组中任选一张卡片，然后点击右上角的「卡片…」（Cards...）按钮。

### 音高重音

最重要的选项莫过于是否在卡片上显示音高重音。目前，关于是否应该学习音高重音，社区里时常有非常激烈的争论。我们选择了一种折衷方案：我们为你提供了音高重音数据，但用不用由你决定。即使你现在选择不用，以后也随时可以开启。开启方法很简单，下面是牌组的「背面模板」（Back Template）代码（点击「搜索」栏上方的小圆点切换）：

```html
<div lang="ja">
{{furigana:Word Furigana}}

<!-- This part enables pitch accent.

{{#Pitch Accent}}
    <br><div style='font-size: 24px'>{{Pitch Accent}}</div>
{{/Pitch Accent}} 

-->

<div style='font-size: 25px; padding-bottom:20px'>{{Word Meaning}}</div>
<div style='font-size: 25px;'>{{furigana:Sentence Furigana}}</div>
<div style='font-size: 25px; padding-bottom:10px'>{{Sentence Meaning}}</div>

{{Word Audio}}
{{Sentence Audio}}
<br>
{{Picture}}

{{#Notes}}
    <br>
    <div style="font-size: 20px; padding-top:12px">Note: {{Notes}}</div>
{{/Notes}}

<!-- This part enables pitch accent notes.

{{#Pitch Accent Notes}}
<div style="font-size: 20px; width: fit-content; max-width:40vw; margin: auto">
    <details><summary>Pitch Accent Notes</summary>
        <br>{{Pitch Accent Notes}}
    </details>
</div>
{{/Pitch Accent Notes}}

-->

</div>
```

要启用音高重音，你只需移除所有代表注释的 `<!--` 和 `-->` 符号即可，就像这样：

```html
<div lang="ja">
{{furigana:Word Furigana}}

{{#Pitch Accent}}
    <br><div style='font-size: 24px'>{{Pitch Accent}}</div>
{{/Pitch Accent}} 

<div style='font-size: 25px; padding-bottom:20px'>{{Word Meaning}}</div>
<div style='font-size: 25px;'>{{furigana:Sentence Furigana}}</div>
<div style='font-size: 25px; padding-bottom:10px'>{{Sentence Meaning}}</div>

{{Word Audio}}
{{Sentence Audio}}
<br>
{{Picture}}

{{#Notes}}
    <br>
    <div style="font-size: 20px; padding-top:12px">Note: {{Notes}}</div>
{{/Notes}}

{{#Pitch Accent Notes}}
<div style="font-size: 20px; width: fit-content; max-width:40vw; margin: auto">
    <details><summary>Pitch Accent Notes</summary>
        <br>{{Pitch Accent Notes}}
    </details>
</div>
{{/Pitch Accent Notes}}

</div>
```

**想了解音高重音的标记方法，请参阅[这个 issue](https://github.com/donkuri/Kaishi/issues/104#issuecomment-3171889366)。**

### 其他次要选项

你还可以调整一些次要选项。

#### 振假名

如果你想移除振假名，只需删除背面模板中的 `furigana:` 部分即可。

#### 其他卡片选项

你也可以随心所欲地改变想要看到的卡片类型。这是 Kaishi 1.5k 的「正面模板」（Front Template）：

```html
<div lang="ja">
{{Word}}
<div style='font-size: 20px;'>{{Sentence}}</div>
</div>
```

如你所见，默认只显示单词和例句。如果你想要**句子**卡片，只需删除 `{{Word}}` 部分，或者用 `{{Sentence}}` 替换它并删除其余部分。如果你想要**单词**卡片，只需删除 `<div style='font-size: 20px;'>{{Sentence}}</div>` 部分。如果你想要**音频**卡片，就删掉所有内容，然后添加 `{{Word Audio}}`、`{{Sentence Audio}}`，或两者皆加。

#### 更改字体、字号或其他样式选项

这是 Kaishi 1.5k 的「样式」（Styling）模板：

```css
.card {
 font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "Noto Sans JP", Osaka, "メイリオ", Meiryo, "ＭＳ Ｐゴシック", "MS PGothic", "MS UI Gothic", sans-serif;
 font-size: 44px;
 text-align: center;
}

img {
max-width: 300px;
max-height: 250px;
}

.mobile img {
max-width: 50vw;
}

/* This part defines the bold color. */
b{color: #5586cd}
```

你可以在[这里](https://docs.ankiweb.net/templates/styling.html)找到各种样式选项。可以看到，Kaishi 1.5k 直接在样式标签页里用的选项很少。你可以修改 `font-family` 来更换字体，`font-size` 来调整字号，`text-align` 来改变文本对齐方式（比如设为左对齐）。默认情况下，Kaishi 1.5k 会给**粗体**文字上色。修改颜色的选项是 `b{color: }`。只需填入一个十六进制颜色代码或颜色名（如 `red`）即可。如果你不想要任何颜色，删掉整行 `b{color: }` 即可。

#### 悬停/点击时显示振假名

可以按照[这个讨论帖](https://github.com/donkuri/kaishi/issues/154)里的方法实现。

### 进阶：自制中→日反向卡片（zh-CN 补充）

> [!NOTE]
> **⚠️ 非上游原版内容：** 本节为 zh-CN 本地化补充，上游原版 README 无此章节。

> [!WARNING]
> **⚠️ 上游作者明确不推荐这样做，请先读完警告再决定。**
> 
> 上游 issue [donkuri/Kaishi#155](https://github.com/donkuri/Kaishi/issues/155)（2026-07）里，社区用户 [JonnaMat](https://github.com/JonnaMat) 提交了完全对应的 “English → Japanese” Card Type 2 教程，本节模板代码即改编自该 issue。上游作者 donkuri 关闭该 issue 时的回复：
> 
> > *“I would highly recommend not doing this as translations are very much one-way streets. Starting from the English sentence, I often would translate it differently.”*
> > 
> > 译：我强烈不建议这样做，因为翻译是单向的。从英文句子出发，我往往会翻译成不同的样子。
> 
> **作者的顾虑：** L2 → L1 的映射不唯一。看到中文“我吃饭”回想日文时，你脑中可能是「ご飯を食べる」，也可能是「食事する」，也可能是「飯を食う」，但卡片只认一个答案，容易造成挫败或强化错误的对应关系。
> 
> 如果你已经理解上述顾虑、仍希望为**特定**词汇启用反向卡（例如已熟悉词想练输出、易混词想强化辨析），继续往下看。

#### 适用场景

- ✅ 已经熟悉正向卡（日→中）、想练输出（写作/口语）
- ✅ 想强化易混词的辨析（如「取る/撮る/採る」）
- ❌ **不适合**：初学者、刚接触该词、只想快速刷识别量
- ❌ **强烈不建议**：一次性给全部 1500 词启用（Anki 会弹 `This will create 1501 cards. Proceed?`，复习量瞬间翻倍，主线节奏被打乱）

**推荐做法：** 批量添加 Card Type 2 后立刻全部 suspend，再按需 unsuspend 特定词（通过 tag、搜索结果或手动挑选）。

#### 添加步骤

1. Anki 主界面 → **浏览** → 左侧选中 Kaishi 卡组 → 随便点一张卡
2. 右上角点 **卡片…** → 卡片类型下拉框右边点 **选项 → 添加卡片类型…**
3. 弹窗提示 `This will create 1501 cards. Proceed?` → 确认
4. 新卡片类型默认名 “Card 2”，建议改为 “反向卡（中→日）” 便于识别
5. 粘贴下面的 Front / Back Template，保存
6. 立刻到 **浏览** 搜 `"反向卡（中→日）"`（或 `"Card 2"`），`Ctrl + A` 全选 → 右键 **切换挂起**，先把 1501 张新卡全部挂起
7. 之后按需 unsuspend 想练的词（如 `word:取る`、`tag:reverse`、`is:due` 等搜索条件）

#### Front Template（正面 = 中文）

只放中文，不放振假名/日文/音频——反向卡的目的就是强迫从中文回想日文：

```html
<div lang="zh-CN">
<div class="cn-font" style='font-size: 30px;'>{{Word Meaning}}</div>
<div class="cn-font" style='font-size: 22px; padding-top: 16px;'>{{Sentence Meaning}}</div>
</div>
```

#### Back Template（背面 = 日文 + 完整反馈）

**直接沿用 Card 1 的 Back Template 即可**（含振假名、音高重音开关、Notes、Pos/Katsuyou 折叠等），无需重写。

> [!TIP]
> **提示：** 如果你在 Card 1 里启用了音高重音（删掉了 `<!--` `-->` 注释），Card 2 的 Back Template 也建议同步启用，保持体验一致。

#### 兼容性说明

- 本节操作完全在你本地 Anki 里进行，**不修改**本仓库分发的 apkg 文件
- 日后导入新版 apkg（例如未来的 v1.4.0）时，Anki 通常会保留你自定义的 Card Type 2；若发现模板或样式被覆盖，按本节步骤重新添加即可
- **导入新版时若不希望模板被覆盖**，可在导入对话框取消勾选 **始终更新笔记模板**——但这样也无法获取上游对 Card 1 的最新修复，需权衡

## 我不想让例句一直显示！

有些人不希望例句一直显示在正面。这个想法完全合理，因为有些人最后只记住了整句。这里保留例句，是为了给你提供语境，毕竟词义永远在具体语境里才有意义。如果你愿意，可以按照[这个 issue 里的评论](https://github.com/donkuri/kaishi/issues/131#issuecomment-3968847411)修改你的正面模板和样式模板，把例句变成模糊状态。感谢 [Hit2Skill](https://github.com/Hit2Skill) 提供的思路！

## 某个词的音频听起来不对！

某些词，比如 **次（つぎ）** 和 **あげる**，被反馈音频“不对”。这是因为初学者往往听不出（也没有意识到）日语的**鼻浊音**现象——/g/ 音听起来会更接近 /n/。关于其原理，请看[这个视频](https://www.youtube.com/watch?v=xpzpbuFHVVU)的解释。**遗憾的是，这些词的非鼻浊音版本（即所谓“更好”的音频）通常并不存在。**

## 如何将 Kaishi 导入到现有牌组之上？

如果你已经开始学习 Core2k 或 Tango N4-N5（或其他类似牌组），又想转而使用 Kaishi 1.5k，可以参考 [Kuuube](https://github.com/Kuuuube) 编写的以下步骤。

1. 使用 .apkg 文件正常导入 Kaishi 牌组。
2. 前往「文件 > 导出…」（File > Export...），选择「笔记（纯文本格式 .txt）」（Notes in Plain Text (.txt)）来导出 Kaishi 牌组，其他设置保持默认。
3. 删除刚刚导入的 Kaishi 牌组。
4. 选中你想并入 Kaishi 的目标牌组，点击「浏览」（Browse），任选一张卡片，按 `ctrl + a` 全选，然后点击左上角菜单的「笔记 > 更改笔记类型…」（Notes > Change Note Type...）。请确保你选中的所有笔记都属于同一种笔记类型，否则该选项可能不会出现。
5. 将笔记类型更改为 `Kaishi 1.5k`。确保「新」（New）列的「Word」字段对应的是你原牌组中表示单词的字段。如果你不打算删除原牌组中任何 Kaishi 未包含的卡片，请确保其他字段也正确对应。否则，直接使用默认设置并点击「保存」（Save）。
6. 导入在第 2 步中导出的 Kaishi .txt 文件。
7. 导入时，确保「笔记类型」设置为 `Kaishi 1.5k`，「牌组」设置为你的目标牌组。如果你打算删除所有非 Kaishi 的卡片，请在「为所有笔记添加标签」（Tag all notes）选项中填入 `Kaishi`。
8. 点击「导入」（Import）。
9. 要删除非 Kaishi 的卡片，请选中你的牌组，点击「浏览」（Browse），在左侧菜单中选中该牌组，然后在搜索框末尾追加 ` -tag:Kaishi`，接着任选一张卡片，按 `ctrl + a` 全选，最后从左上角菜单进入「笔记 > 删除」（Notes > Delete）。

**如果你要导入的目标是 Core 2.3k，请参考[这个链接](https://github.com/Manhhao/anki.transfer-review-history)。**

## 我不喜欢这些图片！

完全可以理解。为这个牌组寻找 1500 张风格统一且可免费使用的图片是一项巨大的挑战（再次感谢 [liarbeast](https://github.com/liarbeast) 的付出！）。因此，许多图片与单词或例句的意境并非完美契合。这是个中肯的批评。如果你想移除图片，可以这样做：在浏览器中点击任意一张 Kaishi 卡片后打开「卡片…」编辑界面，找到「背面」（Back）模板，然后将里面的 `{{Picture}}` 字段删除即可。或者，你也可以直接用以下代码替换整个模板：

```html
<div lang="ja">
{{furigana:Word Furigana}}

<!-- This part enables pitch accent.

{{#Pitch Accent}}
    <br><div style='font-size: 24px'>{{Pitch Accent}}</div>
{{/Pitch Accent}} 

-->

<div style='font-size: 25px; padding-bottom:20px'>{{Word Meaning}}</div>
<div style='font-size: 25px;'>{{furigana:Sentence Furigana}}</div>
<div style='font-size: 25px; padding-bottom:10px'>{{Sentence Meaning}}</div>

{{Word Audio}}
{{Sentence Audio}}
<br>

{{#Notes}}
    <br>
    <div style="font-size: 20px; padding-top:12px">Note: {{Notes}}</div>
{{/Notes}}

<!-- This part enables pitch accent notes.

{{#Pitch Accent Notes}}
<div style="font-size: 20px; width: fit-content; max-width:40vw; margin: auto">
    <details><summary>Pitch Accent Notes</summary>
        <br>{{Pitch Accent Notes}}
    </details>
</div>
{{/Pitch Accent Notes}}

-->

</div>
```

## 牌组的诞生故事

本牌组的诞生，源于我和 Tyogin 在 [TMW discord 服务器](https://learnjapanese.moe/join/) 上的一次讨论。我们都对当时流行的几款初学者牌组中那些恼人的缺陷感到惋惜。由于种种问题，许多初学者在使用 Core 2k 和 Tango 时常常感到困惑。Tango 牌组中包含一些生僻词，比如「ナンプラー」（一种泰国鱼露），而且很多人对牌组中充斥着大量基础短语和国家名并不感兴趣。此外，它的字段格式设计得极差，导致用户几乎无法以其预设的「句子卡片」之外的任何方式使用。而 Core 2k 虽然是模块化的，却存在不少翻译错误、图片缺失或不相关的问题，有些例句也并不实用，甚至无法准确反映所用单词的含义。

这些问题都非常恼人，以至于差不多每两周就有新手向我们提问。于是 Tyogin 提议，不如我们自己动手解决这些问题吧。一个小型团队就此成立。我们主要整合了来自 Core2k、Core10k、Tango N4 和 Tango N5 的数据，然后使用多种 Yomichan/Yomitan 词频词典对单词进行排序，并从中挑选了约 1500 个词。接着，我们修正了每个单词的翻译，为其挑选了最合适的例句，并对需要修改的例句进行了调整（在挑选的 1500 个例句中，我们修正了大约 120 个）。随后，我们从 [AJT Japanese](https://ankiweb.net/shared/info/1344485230) 为那些缺少合适音频的单词获取了音高重音数据和单词音频，并由 Karifurai 和 cindsa 两人团队对音高重音数据进行了核对，还为有需要的单词添加了音高重音笔记。我们还裁剪了音频中的静音部分，并统一了各音频文件之间的音量。此外，我们同样利用 AJT Japanese 为单词和例句生成了振假名。在此之后，我们设计了一套简洁的、以提示为目标的句子卡片 CSS 样式，用于牌组的默认版本。最后，多位成员对牌组进行了校对，以确保错误降到最低。

Kaishi，写作「開始」，意为「开始、开端」。我们觉得这个名字非常贴切，便定了下来。希望这个牌组能为你的日语学习之旅开启一个美妙的篇章。

## 学完本牌组后该做什么？

如果你还没开始，现在就去[开始挖掘（mining）](https://donkuri.github.io/learn-japanese/guide/#consuming-native-content)吧。关于可用的挖掘笔记类型列表，请参阅[这里](https://github.com/donkuri/japanese-resources/?tab=readme-ov-file#mining)。

## 牌组的多语言翻译

如果你有兴趣将本牌组翻译成你的母语，请在 [GitHub 的 issue 追踪器](https://github.com/donkuri/Kaishi/issues)上提出。本牌组已被翻译成 **[俄语](https://github.com/NeonGooRoo/KaishiRu)**、**[印尼语](https://ankiweb.net/shared/info/1512066033)**、**[越南语](https://github.com/duy103zxc/kaishi-vi/releases)**、**[乌克兰语](https://github.com/maksiksq/KaishiUa)**、**[巴西葡萄牙语](https://github.com/nonsolvent/Kaishi-pt-BR)**、**[西班牙语](https://github.com/Dogi5/Kaishi-ESP)**、**[中文](https://github.com/maimemo/kaishi-zh-cn/)**、**[法语](https://github.com/khmskhmskhms/kaishi-FR)**、**[阿拉伯语](https://github.com/kaihouguide/kaishi-arabic)** 和 **[德语](https://github.com/Yukitoki97900/Kaishi-1.5K-German-Version)**。

> [!NOTE]
> **⚠️ 非上游原版内容：** 上游列出的「中文」链接指向老仓库 [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn)。本仓库是[Angle-AOB/kaishi-1.5k-zh-cn](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn) 。

## 从老版本 zh-CN 升级到本仓库版本（zh-CN 补充）

> [!NOTE]
> **⚠️ 非上游原版内容：** 本节为 zh-CN 本地化补充，上游原版 README 无此章节。

如果你之前用的是老仓库 [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn)（v1.3.0，对应上游 v2.2.7 数据），想升级到本仓库 v1.3.0.1（对应上游 v2.4.3）：

1. **先备份**：Anki → **文件 → 导出**，勾选 **包含调度信息**，导出老卡组
2. 下载本仓库最新的 `Kaishi_15k_zh-CN_updated.apkg`
3. Anki → **文件 → 导入**，导入设置勾选：
   - **合并笔记模板**
   - **始终更新笔记**
   - **始终更新笔记模板**
4. 确认导入结果应显示：**109 条笔记已更新**，同时 `tozan.png`、`ojiisanS2.mp3` 两个新媒体文件自动写入媒体库
5. 老版本遗留的 `speed_slow_turtle-*.webp` 与 `ojiisanS.mp3` 会成为孤立媒体（不再被任何卡片引用），不影响使用；如需清理，走 **工具 → 检查媒体**

详细变更清单（哪些词的音高改了、哪些例句改了、哪些新增了注释）见 [CHANGELOG.md](./CHANGELOG.md)。

## 致谢

本牌组的制作离不开以下成员的帮助：

[栗](https://github.com/donkuri/) - 总负责人，负责所有技术、翻译和校对工作

Tyogin - 总负责人，重新排序了前 200 张卡片，修改了例句，并参与校对

shoui - 校对了整个牌组，并修正了翻译

Julian - 协助添加笔记并核对部分例句翻译

karifurai - 核对了前 750 张卡片的音高重音并添加了音高笔记

cindsa - 核对了后 750 张卡片的音高重音并添加了音高笔记

[Kuuube](https://github.com/Kuuuube) - 建议使用 FFmpeg，并撰写了上文关于迁移卡片至 Kaishi 1.5k 的教程

[stephenmk](https://github.com/stephenmk) - 使用 Jmdict Furigana 工具修复了 Kaishi 1.5k 的振假名问题（详见 v1.3.0）

[Kaanium](https://github.com/kaanium) - 协助编写脚本，将牌组转换为书写练习版本

[Lars](https://github.com/liarbeast) - 从 [irasutoya](https://www.irasutoya.com/) 网站添加了图片

在牌组制作过程中，我们使用了以下工具：

[AJT Japanese](https://github.com/Ajatt-Tools/Japanese) - 音高重音、振假名和部分音频通过此插件生成

[FFmpeg](https://ffmpeg.org/) - 用于移除音频文件中的静音片段

[Tenacity](https://tenacityaudio.org/) - 用于编辑音频文件中的爆音

我们还从 TMW discord 服务器的许多成员那里获得了宝贵的建议，其中就包括牌组的名字。牌组中的例句则来源于 AnkiWeb 上的各种 Core 系列牌组。

### zh-CN 本地化

> [!NOTE]
> **⚠️ 非上游原版内容：** 以下致谢为 zh-CN 本地化补充。

- **[maimemo](https://github.com/maimemo)** — 老仓库维护者，完成 v1.0 ~ v1.3.0 的中文释义、词性、活用形翻译，奠定 zh-CN 本地化基础
- **本仓库维护者** — 从 v1.3.0.1 起接管，同步上游 v2.2.7 → v2.4.3 的客观数据修正，翻译上游新增的注释与音高说明

## 反馈与贡献（zh-CN 补充）

> [!NOTE]
> **⚠️ 非上游原版内容：** 本节为 zh-CN 本地化补充。

- **数据问题**（音高、例句、图片、音频、词汇注释）：请到 [上游 donkuri/Kaishi issues](https://github.com/donkuri/Kaishi/issues) 反馈，本仓库会跟随上游同步
- **中文翻译问题**（释义、词性、活用形、注释翻译）：请到 [本仓库 issues](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn/issues) 和 [老仓库 issues](https://github.com/maimemo/kaishi-zh-cn/issues) 反馈
