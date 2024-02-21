import { ActionRowBuilder, TextInputBuilder } from "discord.js";

export const arranger_comp = new TextInputBuilder()
  .setCustomId("arranger_input") // Unique identifier for the text input
  .setPlaceholder("Enter your title here") // Placeholder text displayed in the input field
  .setMaxLength(200); // Maximum character length for the input

export const arranger_input =
  new ActionRowBuilder<TextInputBuilder>().addComponents(arranger_comp);
