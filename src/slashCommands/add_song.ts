import {
  SlashCommandBuilder,
  CacheType,
  ChatInputCommandInteraction,
  ButtonBuilder,
  ActionRowBuilder,
} from "discord.js";
import { SlashCommand } from "../types";
import add_song from "../services/add_song";
import { KeySelection, key_buttons } from "../components/key_button";
import {
  create_conditional_buttons,
  eval_conditional_buttons,
} from "../components/conditional_button";
import { download } from "../utils/download";

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

        interaction.reply("Song added successfully!");
      } else {
        interaction.reply("Information is incorrect. Please try again.");
      }
    } catch (error) {
      console.error("Error occurred:", error);
      interaction.reply("An error occurred while processing your request.");
    }
  },
};

async function promptUserForCollection(
  interaction: ChatInputCommandInteraction<CacheType>
) {
  console.log("Prompting user for collection");
  // Prompt user for collection
  const collection = await interaction.reply({
    content: "Please specify the collection:",
    fetchReply: true,
  });
  console.log(collection);

  // Return user's response
  return collection.content;
}

async function promptUserForTitle(
  interaction: ChatInputCommandInteraction<CacheType>
) {
  // Prompt user for title
  const title = await interaction.reply({
    content: "Please specify the title of the song:",
    fetchReply: true,
  });

  // Return user's response
  return title.content;
}

async function promptUserForKey(
  interaction: ChatInputCommandInteraction<CacheType>
): Promise<KeySelection> {
  let files: KeySelection | null = null;

  do {
    // Prompt user to select the key of the song
    await interaction.reply({
      content: "Please select the key of the song:",
      components: [key_buttons],
    });

    // Wait for user's response
    const keyResponse = await interaction.channel!.awaitMessageComponent({
      filter: (interaction) => interaction.isButton(),
      time: 90000, // Timeout after 90 seconds
    });

    // Add selected key to files
    const selectedKey = keyResponse.customId;
    files = { key: selectedKey, buffer: null };

    // Prompt user to upload a PDF
    await interaction.reply({
      content: "Please upload the PDF for this key:",
    });

    // Wait for user to upload the PDF
    const fileResponse = await interaction.channel!.awaitMessageComponent({
      filter: (interaction) =>
        interaction.isMessageComponent() &&
        interaction.message.attachments.size > 0,
      time: 90000, // Timeout after 90 seconds
    });

    // Add uploaded file to files
    const attachment = fileResponse.message.attachments.first();
    if (attachment) {
      const fileBuffer = await download(attachment.url);
      files.buffer = fileBuffer;
    } else {
      // If no file is uploaded, prompt the user again to select a key
      await interaction.reply({
        content: "Please upload a PDF file for the selected key.",
      });
      continue;
    }
  } while (!files);

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
      const composer = await interaction.reply({
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
      const arranger = await interaction.reply({
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
      const performer = await interaction.reply({
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
  const confirmation = await interaction.reply({
    content: `Please confirm:\nCollection: ${collection}\nTitle: ${title}\nKeys: ${keys}\n\nComposers: ${composerString}\nArrangers: ${arrangerString}\nPerformers: ${performerString}\n\nIs this information correct?`,
    fetchReply: true,
  });

  // Return true if user confirms, false otherwise
  return confirmation.content.toLowerCase().startsWith("y");
}

export default command;
