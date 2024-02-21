import {
  APIApplicationCommandOptionChoice,
  StringSelectMenuBuilder,
  StringSelectMenuOptionBuilder,
} from "discord.js";

export enum Key {
  C = "C",
  Db = "Db",
  D = "D",
  Eb = "Eb",
  E = "E",
  F = "F",
  Gb = "Gb",
  G = "G",
  Ab = "Ab",
  A = "A",
  Bb = "Bb",
  B = "B",
}

export const key_choices = new StringSelectMenuBuilder()
  .setCustomId("select_key")
  .setPlaceholder("Select a key")
  .addOptions(
    Object.values(Key).map((key) =>
      new StringSelectMenuOptionBuilder().setLabel(key).setValue(key)
    )
  );
