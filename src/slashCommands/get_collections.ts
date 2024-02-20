import {
  SlashCommandBuilder,
  ChannelType,
  TextChannel,
  EmbedBuilder,
} from "discord.js";
import { getThemeColor } from "../functions";
import { SlashCommand } from "../types";

export const command: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("get_collections")
    .setDescription(
      "Retrieve the names of the song collections currently available in blowbot's database!"
    ),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 2,
};

export default command;
