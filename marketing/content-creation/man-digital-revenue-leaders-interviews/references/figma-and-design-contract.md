# Figma and design contract

## Approved interview article frames

- Sample-answer layout reference: [node 40001584:2386](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40001584-2386&m=dev)
- Desktop article: [node 40001574:2376](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40001574-2376&m=dev)
- Mobile article: [node 40001577:2386](https://www.figma.com/design/IOhToZi5UBH5vNFV741HP3/MD-Website?node-id=40001577-2386&m=dev)

Related series pages are separate implementations. Do not turn an interview post into a theme or duplicate their chrome inside the post body:

- Series entry frames: nodes `40001490:2359` and `40001490:9083`
- Landing/library frames: nodes `40001505:2384`, `40001556:2376`, and `40001580:31755`

## Visual rules

- Marketing-web surface. Montserrat is used for questions/headings; Lato is used for answers, metadata, and controls.
- Anchor color: `#000FC4`; Ghost White: `#F7F7FF`; cyan accent: `#2DE4E6`; readable dark copy: `#0A0A0A`/`#434343`.
- Structure first: clear article rhythm, generous whitespace, restrained cards, no gradients, frosted glass, emoji, generic SaaS decoration, or fabricated assets.
- Preserve the existing HubSpot blog header/footer and table-of-contents module. The post owns only the intro/body presentation.

## Known-good article measurements

Desktop:

- Question: Montserrat 700, `32px/38.4px`, with a `40px` blue Q marker and `16px` gap.
- Answer: Lato 400, `24px/36px`, `52px` left inset, `16px` paragraph gap.
- Q/A block: `56px` vertical margin, `16px` internal gap.
- TOC links: Lato `22px/33px`, white on the existing blue module.

Mobile (`max-width: 767px`):

- Question: Montserrat 700, `28px/33.9px`, with a `32px` Q marker and `12px` gap.
- Answer: Lato 400, `22px/33px`, no left inset.
- Q/A block: `40px` vertical margin, `12px` internal gap.
- TOC links: Lato `18px/27px`.

## Component contract

- `.rli-intro`: guest portrait, name/role, visible LinkedIn icon/link, short editorial introduction.
- `.rli-sample-notice`: mandatory visible warning for `draft-sample-answers` content.
- `.rli-approval-notice`: mandatory visible warning for transcript-reviewed content that still awaits guest/editorial approval.
- `.rli-video`: optional responsive 16:9 YouTube wrapper that spans the full blog-body width with a transparent wrapper and an iframe that fills it. Use only the `youtube-nocookie.com` embed recorded in the source manifest; never autoplay.
- `.rli-qa`: exactly one `.rli-question` and one `.rli-answer`; stable unique question ID for TOC/deep linking.
- `.rli-pull-quote`: image, quote, attribution, and an editorial state. Unverified quotes remain visibly draft-only.
- `.rli-takeaways`: concise synthesis; do not introduce facts not present in approved answers.
- `.rli-guest-card`: verified portrait, name, role/company, approved bio, and LinkedIn action.

Figma defines the visual treatment, not a reusable question script. Select 7 or 8 questions from the strongest answerable themes in the source. Store `questionSelectionMethod: "source-adapted"`, the Figma frame as `designReference`, and the exact ordered strings as `questions` in interview metadata. The rendered `.rli-question` text and order must match that list exactly.

## Responsive QA

Check at least one desktop, tablet, and mobile viewport in the actual HubSpot preview. Confirm:

- question wording and order match the selected metadata and the count is 7 or 8;
- answer copy does not collide with the Q marker;
- the table of contents is readable and links resolve;
- portraits and title card load without distortion;
- the optional YouTube embed is responsive, full-width within the blog body, transparent around the iframe, titled, privacy-enhanced, and matches the source manifest;
- both LinkedIn actions show the SVG and open the verified profile;
- no horizontal overflow, clipped text, broken images, or template CSS leakage.
