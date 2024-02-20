import {
  SlashCommandBuilder,
  ChannelType,
  TextChannel,
  EmbedBuilder,
} from "discord.js";
import { getThemeColor } from "../functions";
import { SlashCommand } from "../types";

const command: SlashCommand = {
  command: new SlashCommandBuilder()
    .setName("get_num_songs")
    // .setDescription(
    //   `Retrieve the number of songs currently in blowbot's database! Takes an optional parameter, collection,
    //     which can be used to only retrieve the number of songs in a specific collection`
    .setDescription(
      `Retrieve the number of songs currently in blowbot's database!`
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
