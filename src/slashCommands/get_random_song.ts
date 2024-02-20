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
    .setName("get_random_song")
    // .setDescription(`Get a random song from blowbot's database! Takes a number
    // of optional parameters:
    // - collection
    // - credits
    // - key
    // - num_pages
    // And will output a png(s) depending on the parameters provided,
    // or an error message if unsuccessful`),
    .setDescription(`Get a random song from blowbot's database!`),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 3,
};

export default command;
