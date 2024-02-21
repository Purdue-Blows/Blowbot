import { APIApplicationCommandOptionChoice } from "discord.js";

/// Returns a string list of all the collections in the database
export function get_collections(): APIApplicationCommandOptionChoice<string>[] {
  var collection_commands: APIApplicationCommandOptionChoice<string>[] = [];
  for (const collection in Collection) {
    collection_commands.push({
      name: collection_to_string(collection),
      value: collection_to_string(collection),
    });
  }
  return collection_commands;
}

export enum Collection {
  REAL_BOOK = "REAL_BOOK",
}

export function collection_to_string(collection: string): string {
  switch (collection) {
    case Collection.REAL_BOOK.toString():
      return "real-book";
    default:
      return collection;
  }
}
