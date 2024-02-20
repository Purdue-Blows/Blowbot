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
    .setName("add_song")
    // .setDescription(`Add a song to the bot's song database. To add a song, you must have the following:
    // - collection
    // - title
    // - key(s)
    // - pdf(s) or png(s)
    // - credits (composer, arranger, performer, etc)
    // If you specify a key, you must upload the pdf(s)/png(s) associated with that key as well
    // `),
    .setDescription("Add a song to the bot's song database."),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(`🏓 Pong! \n 📡 Ping: ${interaction.client.ws.ping}`)
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 10,
};

export default command;
