import {
  SlashCommandBuilder,
  ChannelType,
  TextChannel,
  EmbedBuilder,
} from "discord.js";
import { getThemeColor } from "../../functions";
import { SlashCommand } from "../../types";

export const get_random_song: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Shows the bot's ping"),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setAuthor({ name: "MRC License" })
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 10,
};
