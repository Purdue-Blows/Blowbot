import { ActionRowBuilder, ModalBuilder, TextInputBuilder } from "discord.js";
import { title_comp, title_input } from "./title_field";
import { collection_selector } from "./collection_button";
import { key_selector } from "./key_button";
import { upload_input } from "./url_field";
import { composer_input } from "./composer_field";
import { arranger_input } from "./arranger_field";
import { performer_input } from "./performer_field";

export const modal = new ModalBuilder()
  .setCustomId("song_input")
  .addComponents(
    collection_selector,
    title_input,
    key_selector,
    upload_input,
    composer_input,
    arranger_input,
    performer_input
  );
