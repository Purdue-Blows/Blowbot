import { ActionRowBuilder, TextInputBuilder } from "discord.js";

export const composer_comp = new TextInputBuilder()
  .setCustomId("composer_input") // Unique identifier for the text input
  .setPlaceholder("Enter your title here") // Placeholder text displayed in the input field
  .setMaxLength(200); // Maximum character length for the input

export const composer_input =
  new ActionRowBuilder<TextInputBuilder>().addComponents(composer_comp);
