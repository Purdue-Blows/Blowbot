import { ActionRowBuilder, TextInputBuilder } from "discord.js";

export const performer_comp = new TextInputBuilder()
  .setCustomId("performer_input") // Unique identifier for the text input
  .setPlaceholder("Enter your title here") // Placeholder text displayed in the input field
  .setMaxLength(200); // Maximum character length for the input

export const performer_input =
  new ActionRowBuilder<TextInputBuilder>().addComponents(performer_comp);
