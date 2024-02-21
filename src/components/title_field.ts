import { ActionRowBuilder, TextInputBuilder } from "discord.js";

export const title_comp = new TextInputBuilder()
  .setCustomId("title_input") // Unique identifier for the text input
  .setPlaceholder("Enter your title here") // Placeholder text displayed in the input field
  .setMaxLength(200); // Maximum character length for the input

export const title_input =
  new ActionRowBuilder<TextInputBuilder>().addComponents(title_comp);
