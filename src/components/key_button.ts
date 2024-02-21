import { ActionRowBuilder, ButtonBuilder } from "discord.js";
import { Key, key_choices } from "../utils/keys";

// Prompt user to select key(s)
export const key_buttons = new ActionRowBuilder<ButtonBuilder>().addComponents(
  key_choices.map((choice) =>
    new ButtonBuilder().setCustomId(choice.value).setLabel(choice.name)
  )
);

export interface KeySelection {
  key: Key | string;
  buffer: Buffer | null;
}
