# Image Placeholders

Marketing assets often need a real photo the brand library cannot supply: a founder/speaker
headshot, a team shot, a product screenshot, or an event photo. Handle these as **labeled
placeholders**, never as flattened stand-ins or AI-faked people.

Image placeholders are the exception, not the build method. The final `.pen` must remain
editable. Do not export the whole design as a flat image and place it back into a canvas or
placeholder. See `editable-pencil-source.md`.

## Rules

- **Check for an existing approved image first.** Look in the design-system `assets/` and
  `uploads/` folders before asking the user — a usable founder headshot or product shot may
  already exist from a prior campaign.
- If the source component already has a screenshot/image placeholder, preserve its structure
  unless the user provides an approved image.
- If the asset needs a real image and none is available, **build a clearly-named placeholder
  frame in the exact slot, at the exact crop ratio** the final image needs, and tell the user
  precisely what belongs there.
- **Never AI-generate a real person's likeness.** A founder/speaker placeholder stays a
  placeholder until the user supplies the real photo.
- For abstract/brand imagery the user explicitly asks to be generated, create or request it
  separately, then place it into the placeholder frame. Do not silently generate imagery inside
  a production asset.
- Use MAN Digital design-system assets first for logos and approved brand visuals.
- Do not use off-brand stock imagery. Icons come from the Streamline-style library already in
  the Playground, not from stock art.
- Do not use a generated image, screenshot, or exported PNG as a replacement for editable Pencil
  text, labels, cards, or decorations.

## Placeholder Crop Hints By Asset

Size and position the placeholder so the user only has to drop one image in:

- **LinkedIn event cover (1776 × 444):** speaker headshot reads as a tall portrait crop on the
  right third, clear of the center event-name safe zone.
- **YouTube thumbnail (1280 × 720):** large face crop, subject right, eyes in the upper third,
  clear of the bottom-right duration-badge zone. Faces drive CTR — keep it ~40% of the frame.
- **LinkedIn personal banner (1584 × 396):** if a photo is used, keep it in the upper-right
  two-thirds, away from the bottom-left avatar overlap (≈568 × 264).
- **Instagram / Facebook portrait post (1080 × 1350):** keep the subject inside the center 3:4
  region so the Instagram grid crop does not trim it.
- **Product shot:** square or transparent-background crop the user can drop onto a card or panel.

## User-Facing Note

When leaving a placeholder, state exactly what belongs there and the crop, for example:

`Founder photo placeholder left in the right third of the event cover: add a high-res headshot,
portrait crop ~3:4, plain or easily-removable background, before publishing.`
