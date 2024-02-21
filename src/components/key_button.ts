import {
  ActionRowBuilder,
  ButtonBuilder,
  StringSelectMenuBuilder,
} from "discord.js";
import { Key, key_choices } from "../utils/keys";

// Prompt user to select key(s)
export const key_selector =
  new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(key_choices);

export interface KeySelection {
  key: Key | string;
  buffer: Buffer | null;
}
