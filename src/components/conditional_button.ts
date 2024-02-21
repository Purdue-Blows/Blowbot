import {
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  CacheType,
  ChatInputCommandInteraction,
  StringSelectMenuBuilder,
  StringSelectMenuOptionBuilder,
} from "discord.js";

// Define the emoji IDs or names for the check and x emojis
const yesEmoji = "✅";
const noEmoji = "❌";

// Prompt user a true or false question
export function create_conditional_buttons(): ActionRowBuilder<ButtonBuilder> {
  const trueButton = new ButtonBuilder()
    .setCustomId("yes")
    .setLabel("Yes")
    .setStyle(ButtonStyle.Success) // Use "SUCCESS" for the success color
    .setEmoji(yesEmoji); // Set the check emoji

  const falseButton = new ButtonBuilder()
    .setCustomId("no")
    .setLabel("No")
    .setStyle(ButtonStyle.Danger) // Use "DANGER" for the danger color
    .setEmoji(noEmoji); // Set the x emoji

  return new ActionRowBuilder<ButtonBuilder>().addComponents(
    trueButton,
    falseButton
  );
}

export async function eval_conditional_buttons(
  interaction: ChatInputCommandInteraction<CacheType>,
  message: string
): Promise<boolean> {
  await interaction.reply({
    content: message,
    fetchReply: true,
    components: [create_conditional_buttons()],
  });

  const response = await interaction.channel!.awaitMessageComponent({
    filter: (interaction) => interaction.isButton(),
    time: 30000, // Timeout after 30 seconds
  });

  // Return true if the user selects "Yes", false otherwise
  return response.customId === "yes";
}

export function createConditionalSelectMenu(
  id: string
): ActionRowBuilder<StringSelectMenuBuilder> {
  const conditionalMenu = new StringSelectMenuBuilder()
    .setCustomId(id)
    .setPlaceholder("Make a selection")
    .addOptions(
      new StringSelectMenuOptionBuilder()
        .setLabel("Yes")
        .setDescription("YES!!!")
        .setValue("yes"),
      new StringSelectMenuOptionBuilder()
        .setLabel("No")
        .setDescription("no...")
        .setValue("no")
    );

  return new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(
    conditionalMenu
  );
}
