import {
  ActionRowBuilder,
  StringSelectMenuBuilder,
  StringSelectMenuOptionBuilder,
} from "discord.js";
import { Collection } from "../utils/collections";

export const collection_choices = new StringSelectMenuBuilder()
  .setCustomId("select_collection")
  .setPlaceholder("Select a collection")
  .addOptions(
    Object.keys(Collection).map((key) =>
      new StringSelectMenuOptionBuilder().setLabel(key).setValue(key)
    )
  );

export const collection_selector =
  new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(
    collection_choices
  );
