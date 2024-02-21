import {
  SlashCommandBuilder,
  CacheType,
  ChatInputCommandInteraction,
  ButtonBuilder,
  ActionRowBuilder,
  Message,
  StringSelectMenuBuilder,
  StringSelectMenuOptionBuilder,
  ComponentType,
} from "discord.js";
import { SlashCommand } from "../types";
import add_song from "../services/add_song";
import { KeySelection, key_selector } from "../components/key_button";
import {
  create_conditional_buttons,
  eval_conditional_buttons,
} from "../components/conditional_button";
import { download } from "../utils/download";
import { collection_selector } from "../components/collection_button";
import { collection_to_string } from "../utils/collections";
import { title_input } from "../components/title_field";

const command: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("add_song")
    .setDescription("Add a song to the bot's song database."),
  execute: async (interaction) => {
    try {
      // Prompt user for collection
      const collection = await promptUserForCollection(interaction);

      // Prompt user for title
      const title = await promptUserForTitle(interaction);

      // Prompt user to select key(s)
      const keys = await promptUserForKey(interaction);

      // Prompt user for composer(s), arranger(s), performer(s)
      const credits = await promptUserForCredits(interaction);

      // Check if the information is correct
      const isInformationCorrect = await confirmInformation(interaction, {
        collection,
        title,
        keys,
        credits,
      });

      if (isInformationCorrect) {
        // Add the song to the database
        add_song(
          collection,
          title,
          keys,
          credits.get("composers") ?? [],
          credits.get("arrangers") ?? [],
          credits.get("performers") ?? []
        );

        interaction.followUp({
          content:
            "successfully added song " + title + " to blowbot's database!",
          ephemeral: false,
        });
      } else {
        interaction.followUp({
          content: "Information is incorrect. Please try again.",
          ephemeral: true,
        });
      }
    } catch (error) {
      console.error("Error occurred:", error);
      interaction.followUp({
        content: "An error occurred while processing your request.",
        ephemeral: true,
      });
    }
  },
};

async function promptUserForCollection(
  interaction: ChatInputCommandInteraction<CacheType>
): Promise<string> {
  try {
    // Send a message to prompt the user for the collection
    await interaction.reply({
      content: "Please select a song collection",
      ephemeral: true,
      fetchReply: true,
      components: [collection_selector],
    });

    // Wait for the user's response
    const collectionInteraction =
      await interaction.channel!.awaitMessageComponent({
        filter: (interaction) =>
          interaction.isStringSelectMenu() &&
          interaction.customId === "select_collection",
        componentType: ComponentType.StringSelect,
        time: 90000, // Timeout after 90 seconds
      });

    // Get the selected value from the interaction
    const selectedCollection = collectionInteraction.values.at(0);
    if (selectedCollection == undefined) {
      throw new Error("Could not select that collection");
    }

    // Update collection value
    if (collectionInteraction.customId === "select_collection") {
      await collectionInteraction.update({
        content: "Collection: " + selectedCollection,
        components: [],
      });
    }

    // Return the selected collection
    return collection_to_string(selectedCollection);
  } catch (error) {
    throw new Error(
      "An error occurred while prompting for collection: " + error.message
    );
  }
}

async function promptUserForTitle(
  interaction: ChatInputCommandInteraction<CacheType>
): Promise<string> {
  try {
    // Create a message filter to collect messages from the same user
    const filter = (message: Message) =>
      message.author.id === interaction.user.id;

    // Send a message to prompt the user for the title
    var title: string = "";
    await interaction.followUp({
      content: "Please specify the title of the song",
      ephemeral: true,
      fetchReply: true,
      components: [title_input],
    });
    const titleInteraction = await interaction.channel!.awaitMessages({
      filter: filter,
      max: 1,
      time: 90000, // 90 second delay
    });

    if (
      !titleInteraction.first()?.content ||
      titleInteraction.first()?.content == ""
    ) {
      throw new Error("Invalid title");
    }
    title = titleInteraction.first()?.content!;

    // Return the user's response
    return title;
  } catch (error) {
    console.error("An error occurred while prompting for title:", error);
    throw new Error("An error occurred while prompting for title.");
  }
}

async function promptUserForKey(
  interaction: ChatInputCommandInteraction<CacheType>
): Promise<KeySelection> {
  let files: KeySelection | null = null;

  // Prompt user to select the key of the song
  await interaction.followUp({
    content: "Please select the key of the song",
    components: [key_selector],
  });

  // Wait for user's response
  const keyResponse = await interaction.channel!.awaitMessageComponent({
    filter: (interaction) =>
      interaction.isStringSelectMenu() && interaction.customId === "select_key",
    componentType: ComponentType.StringSelect,
    time: 90000, // Timeout after 90 seconds
  });

  // Add selected key to files
  const selectedKey = keyResponse.values.at(0);
  if (selectedKey == undefined) {
    throw new Error("Could not select that key");
  }
  files = { key: selectedKey, buffer: null };

  // Update value
  if (keyResponse.customId === "select_key") {
    await keyResponse.update({
      content: "Key: " + selectedKey,
      components: [],
    });
  }

  // Prompt user to upload a PDF
  await interaction.followUp({
    content: "Please upload the PDF for this key",
    ephemeral: true,
  });

  // Wait for user to upload the PDF
  const fileResponse = await interaction.channel!.awaitMessageComponent({
    filter: (interaction) =>
      interaction.isMessageComponent() &&
      interaction.message.attachments.size > 0 &&
      interaction.message.attachments.first()?.contentType ===
        "application/pdf",
    time: 90000, // Timeout after 90 seconds
  });

  // Add uploaded file to files
  const attachment = fileResponse.message.attachments.first();
  console.log(attachment);
  if (attachment) {
    const fileBuffer = await download(attachment.url);
    files.buffer = fileBuffer;
  } else {
    // If no file is uploaded, prompt the user again to select a key
    throw new Error("Could not download that pdf file");
  }

  // Return the selected key and its associated file buffer
  return files;
}

async function promptUserForCredits(
  interaction: ChatInputCommandInteraction<CacheType>
): Promise<Map<string, string[]>> {
  const credits: Map<string, string[]> = new Map();

  // Prompt user for composer(s)
  const isComposer = await eval_conditional_buttons(
    interaction,
    "Do you know the composer(s)?"
  );

  if (isComposer) {
    const composers: string[] = [];
    do {
      const composer = await interaction.followUp({
        content: "Specify the composer(s)",
        fetchReply: true,
      });
      composers.push(composer.content);
    } while (
      await eval_conditional_buttons(interaction, "Is there another composer?")
    );
    credits.set("composers", composers);
  }

  // Prompt user for arranger(s)
  const isArranger = await eval_conditional_buttons(
    interaction,
    "Do you know the arranger(s)?"
  );

  if (isArranger) {
    const arrangers: string[] = [];
    do {
      const arranger = await interaction.followUp({
        content: "Specify the arranger(s)",
        fetchReply: true,
      });
      arrangers.push(arranger.content);
    } while (
      await eval_conditional_buttons(
        interaction,
        "Is there another arranger(s)?"
      )
    );
    credits.set("arrangers", arrangers);
  }

  // Prompt user for performer(s)
  const isPerformer = await eval_conditional_buttons(
    interaction,
    "Do you know the performer(s)?"
  );

  if (isPerformer) {
    const performers: string[] = [];
    do {
      const performer = await interaction.followUp({
        content: "Specify the performer(s)",
        fetchReply: true,
      });
      performers.push(performer.content);
    } while (
      await eval_conditional_buttons(interaction, "Is there another performer?")
    );
    credits.set("performers", performers);
  }

  return credits;
}

async function confirmInformation(
  interaction: ChatInputCommandInteraction<CacheType>,
  {
    collection,
    title,
    keys,
    credits,
  }: {
    collection: string;
    title: string;
    keys: KeySelection;
    credits: Map<string, string[]>;
  }
) {
  // Format credits map into strings for each category
  const composerString = credits.has("composer")
    ? credits.get("composer")!.join(", ")
    : "None";
  const arrangerString = credits.has("arranger")
    ? credits.get("arranger")!.join(", ")
    : "None";
  const performerString = credits.has("performer")
    ? credits.get("performer")!.join(", ")
    : "None";

  // Prompt user to confirm the information
  const confirmation = await interaction.followUp({
    content: `Please confirm:\nCollection: ${collection}\nTitle: ${title}\nKeys: ${keys}\n\nComposers: ${composerString}\nArrangers: ${arrangerString}\nPerformers: ${performerString}\n\nIs this information correct?`,
    fetchReply: true,
  });

  // Return true if user confirms, false otherwise
  return confirmation.content.toLowerCase().startsWith("y");
}

export default command;
