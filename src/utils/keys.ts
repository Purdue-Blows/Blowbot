import { APIApplicationCommandOptionChoice } from "discord.js";

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

export const key_choices: APIApplicationCommandOptionChoice<string>[] =
  Object.values(Key).map((key) => ({
    name: key,
    value: key,
  }));
