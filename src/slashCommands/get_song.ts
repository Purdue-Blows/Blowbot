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
    .setName("get_song")
    // .setDescription(`Retrieve a song using specific parameters, including:
    // - collection
    // - id
    // - key
    // You should get_song_info before this command if you're not sure what the id of your
    // desired song is
    // `),
    .setDescription(`Retrieve a song from blowbot's database!`),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 5,
};

export default command;
