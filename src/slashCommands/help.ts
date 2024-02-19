import {
  SlashCommandBuilder,
  ChannelType,
  TextChannel,
  EmbedBuilder,
} from "discord.js";
import { getThemeColor } from "../functions";
import { SlashCommand } from "../types";

const help: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("help")
    .setDescription("Get some help"),
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

export default help;
