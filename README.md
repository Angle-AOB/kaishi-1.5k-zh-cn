**本仓库并非上游官方仓库，仅为 Kaishi 1.5k 的简体中文本地化衍生版本；如发现数据错误，请先分清是「上游客观数据问题」还是「中文翻译问题」，再到对应仓库反馈。**

# Kaishi 1.5k zh-CN

面向中文母语者的日语入门 Anki 卡组，本地化自上游 [donkuri/Kaishi](https://github.com/donkuri/Kaishi)。当前数据基线 **v2.4.3**，zh-CN 本地化版本 **v1.5.0**。

## 项目关系

| 类型 | 仓库 | 版本 | 说明 |
| --- | --- | --- | --- |
| 上游 | [donkuri/Kaishi](https://github.com/donkuri/Kaishi) | v2.4.3 | 客观数据来源（音高重音、例句、配图、音频、词汇注释） |
| zh-CN 老仓库 | [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn) | v1.4.0 | 早期（v2.2.7）中文本地化仓库，提供中文释义、词性、活用形的基础翻译 |
| 本仓库 | [Angle-AOB/kaishi-1.5k-zh-cn](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn) | v1.5.0 起 | 从老仓库派生，提供后续 zh-CN 本地化迭代与上游同步 |
| 更新日志 | [CHANGELOG.md](./CHANGELOG.md) | — | 每次发布的详细变更（同步了哪些上游数据、翻译了哪些新增注释、升级路径等） |

**双版本号约定：** CHANGELOG 里标题形如 `## v1.5.0（上游版本 v2.4.3）`——前者是 zh-CN 本地化版本，延续老仓库 v1.x 体系；后者是数据同步基线，与上游 v2.x 对齐。两条版本线并行，不合并、不同步。

---

## 卡组简介

Kaishi 1.5k 是一套为日语初学者设计的现代 Anki 卡组，收录约 1500 个高频基础词汇。卡组高度模块化，本页说明可以按需自定义的各种选项。卡组正面如下：

<img src="https://github.com/donkuri/Kaishi/blob/main/pics/kaishi-front.png" alt="Kaishi 1.5k 卡片正面" style="width: 100%; height: auto">

正面同时显示单词与例句，但例句里的目标单词会被高亮加粗，方便一眼锁定重点；等单词熟悉之后，因为单词先出现，复习速度会显著变快。卡组背面如下：

<img src="https://github.com/donkuri/Kaishi/blob/main/pics/kaishi-back.png" alt="Kaishi 1.5k 卡片背面" style="width: 100%; height: auto">

与常见的 Core 类卡组不同，Kaishi 背面优先显示振假名标注的读音，释义紧跟其下，然后是单词音频、例句音频、可选配图，最后是可选的音高重音与卡片专属注释。

> **日语新手请先阅读学习指南：** <https://donkuri.github.io/learn-japanese/guide/>（英文，可用浏览器翻译）。Kaishi 只是学习路径中的一环，不建议单独依赖。

### 目录

- [在哪里下载卡组？](#在哪里下载卡组)
- [zh-CN 版本比上游多了什么？](#zh-cn-版本比上游多了什么)
- [卡组有哪些可自定义选项？](#卡组有哪些可自定义选项)
  - [音高重音](#音高重音)
  - [振假名](#振假名)
  - [切换卡片类型（词卡/句卡/音卡）](#切换卡片类型词卡句卡音卡)
  - [进阶：自制中→日反向卡片](#进阶自制中日反向卡片)
  - [字体、字号与其他样式](#字体字号与其他样式)
  - [悬停/点击才显示振假名](#悬停点击才显示振假名)
- [我不想让例句一直显示！](#我不想让例句一直显示)
- [某个词的音频听起来不对！](#某个词的音频听起来不对)
- [如何把 Kaishi 覆盖导入到已有卡组？](#如何把-kaishi-覆盖导入到已有卡组)
- [我不喜欢配图！](#我不喜欢配图)
- [卡组的由来](#卡组的由来)
- [刷完 Kaishi 之后做什么？](#刷完-kaishi-之后做什么)
- [其他语言的翻译版本](#其他语言的翻译版本)
- [从老版本 zh-CN 升级到本仓库版本](#从老版本-zh-cn-升级到本仓库版本)
- [致谢](#致谢)

---

## 在哪里下载卡组？

- **本仓库（zh-CN 最新版）：** [Releases 页面](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn/releases) 下载 `Kaishi_15k_zh-CN_updated.apkg`
- **老仓库（zh-CN v1.4.0）：** <https://github.com/maimemo/kaishi-zh-cn>
- **上游（日文原版）：** [donkuri/Kaishi Releases](https://github.com/donkuri/Kaishi/releases/) 或 [AnkiWeb](https://ankiweb.net/shared/info/1196762551)

**最低 Anki 版本：2.1.50+**（低于此版本可能因模板语法或字段变化而导入失败）。

导入方法：Anki → **文件 → 导入** → 选择 `.apkg`。若之前已经装过老版本 zh-CN，请参考本文末尾的[升级章节](#从老版本-zh-cn-升级到本仓库版本)。

---

## zh-CN 版本比上游多了什么？

本仓库在完整继承上游客观数据的前提下，为中文母语者增加了以下内容：

| 字段 | 上游原版 | 本仓库 zh-CN 版 |
| --- | --- | --- |
| `Word Meaning` | 英文释义 | **中文释义**（保留老仓库翻译，部分调整） |
| `Sentence Meaning` | 英文翻译 | **中文翻译** |
| `Notes` | 英文注释 | **中文注释**（上游新增注释同步翻译） |
| `Pitch Accent Notes` | 英文音高说明 | **中文音高说明**（含鼻浊音、音高变化等语言现象的详细解释） |
| `Pos`（Field 14） | 无 | **中文词性标注**（zh-CN 独有字段） |
| `Katsuyou`（Field 15） | 无 | **中文活用形说明**（zh-CN 独有字段，标注动词/形容词的活用类型） |

上游的音高重音数据（`Pitch Accent`）、例句（`Sentence`、`Sentence Furigana`）、图片（`Picture`）、音频（`Word Audio`、`Sentence Audio`）等客观字段与上游 v2.4.3 完全一致，未做本地化改写。

> **注意：** 卡片模板（Front/Back/CSS）默认与上游一致，`Pos` 与 `Katsuyou` 字段虽然存在，但不会自动显示在卡片上。如需展示，请自行在 Back Template 里加入 `{{Pos}}`、`{{Katsuyou}}`。

---

## 卡组有哪些可自定义选项？

修改方法：在 Anki 主界面选中 Kaishi 卡组 → 点击 **浏览** → 任选一张卡片 → 右上角点击 **卡片…**。

### 音高重音

要不要学音高重音，是日语学习社区里长期争论的话题。Kaishi 采取折中方案：**数据已经准备好了，是否显示由你决定**；即便现在关闭，将来想开启也随时可以。

Back Template 里默认把音高重音相关部分用 HTML 注释包起来了：

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

**启用音高重音：** 删掉 `<!--` 与 `-->`（两处注释块都删），保存即可：

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

**音高记号规则说明：** 详见上游 issue [donkuri/Kaishi#104](https://github.com/donkuri/Kaishi/issues/104#issuecomment-3171889366)（英文）。

### 振假名

想去掉振假名？把 Back Template 里所有 `furigana:` 前缀删掉即可，例如：

- `{{furigana:Word Furigana}}` → `{{Word Furigana}}`
- `{{furigana:Sentence Furigana}}` → `{{Sentence Furigana}}`

### 切换卡片类型（词卡/句卡/音卡）

Front Template 默认如下：

```html
<div lang="ja">
{{Word}}
<div style='font-size: 20px;'>{{Sentence}}</div>
</div>
```

- **只想看句卡：** 删掉 `{{Word}}`，或把整块替换为 `{{Sentence}}`
- **只想看词卡：** 删掉 `<div style='font-size: 20px;'>{{Sentence}}</div>`
- **只听音频：** 整块替换为 `{{Word Audio}}`、`{{Sentence Audio}}`，或两者都写

### 进阶：自制中→日反向卡片

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

> **提示：** 如果你在 Card 1 里启用了音高重音（删掉了 `<!--` `-->` 注释），Card 2 的 Back Template 也建议同步启用，保持体验一致。

#### 兼容性说明

- 本节操作完全在你本地 Anki 里进行，**不修改**本仓库分发的 apkg 文件
- 日后导入新版 apkg（例如未来的 v1.6.0）时，Anki 通常会保留你自定义的 Card Type 2；若发现模板或样式被覆盖，按本节步骤重新添加即可
- **导入新版时若不希望模板被覆盖**，可在导入对话框取消勾选 **始终更新笔记模板**——但这样也无法获取上游对 Card 1 的最新修复，需权衡

### 字体、字号与其他样式

Styling 模板默认：

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

常见调整：

- `font-family` 换字体（Windows 用户可加 `"Microsoft YaHei"`、`"Yu Gothic"` 等）
- `font-size` 改字号
- `text-align` 改对齐（`left` 左对齐、`center` 居中）
- `b{color: #5586cd}` 改例句里高亮单词的颜色，替换成任意十六进制色号或颜色名（如 `red`）；不想高亮就整块删掉

更多 CSS 选项参考 Anki 官方文档：<https://docs.ankiweb.net/templates/styling.html>

### 悬停/点击才显示振假名

见上游 issue [donkuri/kaishi#154](https://github.com/donkuri/kaishi/issues/154)（英文）。

---

## 我不想让例句一直显示！

有人担心一直看着例句，最后记住的是整句而不是单词——这个顾虑是合理的。Kaishi 保留例句是因为**词义永远在具体语境里才有意义**。如果你确实想遮挡例句，可以按照上游 issue [donkuri/kaishi#131](https://github.com/donkuri/kaishi/issues/131#issuecomment-3968847411) 里的方案改 Front Template 和 Styling，让例句变成模糊状态，鼠标悬停或点击才清晰显示。感谢 [Hit2Skill](https://github.com/Hit2Skill) 提供的思路。

---

## 某个词的音频听起来不对！

比如 **次（つぎ）**、**あげる**、**上げる**、**動く** 这类词，常有学习者反馈音频"听起来像 ni / ani"。这不是音频错误，而是日语的**鼻浊音**现象——/g/ 音在词中或词尾时，母语者常发成带鼻音的 [ŋ]，听感接近 /n/。中文里没有这个音位对立，所以初学者容易忽略。

推荐看这个视频理解鼻浊音：<https://www.youtube.com/watch?v=xpzpbuFHVVU>（YouTube；也可搜"日本語 鼻濁音"找中文讲解）。

**遗憾的是，非鼻浊音版本的清晰音频通常并不存在**，因为这些词的自然发音就是鼻浊音。本仓库已在 `Notes` 或 `Pitch Accent Notes` 字段为相关词条补充了中文说明，并附上视频链接。

---

## 如何把 Kaishi 覆盖导入到已有卡组？

如果你已经开始刷 Core 2k、Tango N4-N5 或类似卡组，想切换到 Kaishi 1.5k，同时**保留原有学习进度**，可以按照 [Kuuube](https://github.com/Kuuuube) 提供的步骤操作（下面从上游 README 翻译）：

1. 正常导入 Kaishi `.apkg`
2. **文件 → 导出**，把 Kaishi 卡组导出为 `Notes in Plain Text (.txt)`，其它设置保持默认
3. 删除刚导入的 Kaishi 卡组
4. 选中你**想被覆盖的卡组**，点击 **浏览**，随便点一张卡，`Ctrl + A` 全选，然后左上角菜单 **笔记 → 更改笔记类型**。确保选中的所有笔记都属于同一个笔记类型，否则该菜单项可能不显示
5. 改成 `Kaishi 1.5k` 笔记类型，确认 **New** 列的 `Word` 字段对应你原卡组里存单词的字段；如果你不打算删除原卡组里 Kaishi 不包含的卡片，其他字段也要一一对齐；否则用默认映射即可，点 **保存**
6. 导入第 2 步导出的 Kaishi `.txt`
7. 导入时把 **笔记类型** 设为 `Kaishi 1.5k`、**卡组** 设为要被覆盖的那个卡组；如果打算删除 Kaishi 不包含的旧卡片，在 **给所有笔记加标签** 里填 `Kaishi`
8. 点击 **导入**
9. 要删除 Kaishi 不包含的旧卡片：选中卡组 → **浏览** → 左侧选中该卡组 → 搜索栏追加 ` -tag:Kaishi` → 任选一张卡 → `Ctrl + A` → 左上角 **笔记 → 删除**

**若要覆盖导入到 Core 2.3k，另需参考 [anki.transfer-review-history](https://github.com/Manhhao/anki.transfer-review-history) 迁移复习历史。**

---

## 我不喜欢配图！

理解。给 1500 个词找一致且可自由使用的图片本身就是巨大挑战（这部分主要由上游的 [liarbeast](https://github.com/liarbeast) 完成），所以确实有些图片与词义或例句对不太上。

要去掉图片：在 **浏览** 里选任意 Kaishi 卡片 → 右上角 **卡片…** → 选 **Back Template** → 找到 `{{Picture}}` 删掉即可。或者干脆用下面这段完整替换 Back Template（同时保留音高重音注释开关）：

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

---

## 卡组的由来

以下内容译自上游 README，简略版本：

Kaishi 起源于 [TMW Discord 服务器](https://learnjapanese.moe/join/) 里 Tyogin 与上游作者 [栗（donkuri）](https://github.com/donkuri/) 的一次讨论。当时主流的初学者卡组（Core 2k、Tango N4-N5）都存在明显问题：Tango 收录了如 ナンプラー（泰式鱼露）这类生僻词，还塞了大量基础短语和国名，字段设计僵硬、只能做句卡；Core 2k 虽然模块化，但存在误译、图片缺失或与词义无关，例句质量也不稳定，甚至有时反映不出词义。

于是他们组建了一个小团队，从 Core 2k、Core 10k、Tango N4、Tango N5 抽取数据，用多个 Yomichan/Yomitan 词频字典重排，选出约 1500 个词。之后逐个校对释义、为每个词挑选最佳例句（其中约 120 条例句需要修复），补充音高重音数据，从 [AJT Japanese](https://ankiweb.net/shared/info/1344485230) 补齐缺失音频，由 karifurai 与 cindsa 两人分工核验前后 750 张卡的音高数据并补充注释。音频经过静音裁剪与响度归一化，振假名也由 AJT Japanese 生成。最后由多人校对通读。

「開始（かいし）」在日语里意为"开始、开端"——希望这套卡组能成为你日语学习旅程的美好起点。

---

## 学完 Kaishi 之后做什么？

**开始挖词（mining）**——从你实际阅读/观看的日语内容里提取生词做成 Anki 卡片。参考：

- 上游指南：<https://donkuri.github.io/learn-japanese/guide/#consuming-native-content>
- 常用挖词笔记类型汇总：<https://github.com/donkuri/japanese-resources/?tab=readme-ov-file#mining>

---

## 其他语言的翻译版本

Kaishi 已被翻译成多种语言，如果你有其他语言需求，可以到对应仓库查看：

- **俄语**：<https://github.com/NeonGooRoo/KaishiRu>
- **印尼语**：<https://ankiweb.net/shared/info/1512066033>
- **越南语**：<https://github.com/duy103zxc/kaishi-vi/releases>
- **乌克兰语**：<https://github.com/maksiksq/KaishiUa>
- **巴西葡萄牙语**：<https://github.com/nonsolvent/Kaishi-pt-BR>
- **西班牙语**：<https://github.com/Dogi5/Kaishi-ESP>
- **中文（本仓库）**：<https://github.com/Angle-AOB/kaishi-1.5k-zh-cn>（继承自 [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn)）
- **法语**：<https://github.com/khmskhmskhms/kaishi-FR>
- **阿拉伯语**：<https://github.com/kaihouguide/kaishi-arabic>
- **德语**：<https://github.com/Yukitoki97900/Kaishi-1.5K-German-Version>

有意翻译到其他语言？请到 [上游 issue tracker](https://github.com/donkuri/Kaishi/issues) 开设新 issue。

---

## 从老版本 zh-CN 升级到本仓库版本

如果你之前用的是老仓库 [maimemo/kaishi-zh-cn](https://github.com/maimemo/kaishi-zh-cn)（v1.4.0，对应上游 v2.2.7 数据），想升级到本仓库 v1.5.0（对应上游 v2.4.3）：

1. **先备份**：Anki → **文件 → 导出**，勾选 **包含调度信息**，导出老卡组
2. 下载本仓库最新的 `Kaishi_15k_zh-CN_updated.apkg`
3. Anki → **文件 → 导入**，导入设置勾选：
   - **合并笔记模板**
   - **始终更新笔记**
   - **始终更新笔记模板**
4. 确认导入结果应显示：**109 条笔记已更新**，同时 `tozan.png`、`ojiisanS2.mp3` 两个新媒体文件自动写入媒体库
5. 老版本遗留的 `speed_slow_turtle-*.webp` 与 `ojiisanS.mp3` 会成为孤立媒体（不再被任何卡片引用），不影响使用；如需清理，走 **工具 → 检查媒体**

详细变更清单（哪些词的音高改了、哪些例句改了、哪些新增了注释）见 [CHANGELOG.md](./CHANGELOG.md)。

---

## 致谢

### 上游 Kaishi 1.5k 团队

- **[栗（donkuri）](https://github.com/donkuri/)** — 主要架构师，负责所有技术方面、翻译与校对
- **Tyogin** — 主要架构师，重排前 200 张卡片，调整例句，校对
- **shoui** — 通读整套卡组校对，修正翻译
- **Julian** — 补充注释，检查部分例句翻译
- **karifurai** — 核验前 750 张卡的音高重音数据并补充音高注释
- **cindsa** — 核验后 750 张卡的音高重音数据并补充音高注释
- **[Kuuube](https://github.com/Kuuuube)** — 建议使用 FFmpeg 处理音频；撰写"覆盖导入到其他卡组"章节
- **[stephenmk](https://github.com/stephenmk)** — 用 Jmdict Furigana 工具修复振假名（见上游 v1.3.0）
- **[Kaanium](https://github.com/kaanium)** — 协助编写脚本，把卡组转换为书写版本
- **[Lars（liarbeast）](https://github.com/liarbeast)** — 从 [いらすとや](https://www.irasutoya.com/) 补充配图

上游使用的工具：

- **[AJT Japanese](https://github.com/Ajatt-Tools/Japanese)** — 生成音高重音、振假名与部分音频
- **[FFmpeg](https://ffmpeg.org/)** — 裁剪音频静音段
- **[Tenacity](https://tenacityaudio.org/)** — 修复音频削波

此外，卡组名称与许多设计灵感来自 TMW Discord 服务器成员；例句则来自 AnkiWeb 上多套 Core 卡组。

### zh-CN 本地化

- **[maimemo](https://github.com/maimemo/kaishi-zh-cn)** — 老仓库维护者，完成 v1.0 ~ v1.4.0 的中文释义、词性、活用形翻译，奠定 zh-CN 本地化基础
- **本仓库维护者** — 从 v1.5.0 起接管，同步上游 v2.2.7 → v2.4.3 的客观数据修正，翻译上游新增的注释与音高说明

---

## 反馈与贡献

- **数据问题**（音高、例句、图片、音频、词汇注释）：请到 [上游 donkuri/Kaishi issues](https://github.com/donkuri/Kaishi/issues) 反馈，本仓库会跟随上游同步
- **中文翻译问题**（释义、词性、活用形、注释翻译）：请到 [本仓库 issues](https://github.com/Angle-AOB/kaishi-1.5k-zh-cn/issues) 反馈
