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
    .setName("help")
    .setDescription("Get some help"),
  execute: (interaction) => {
    interaction.reply({
      embeds: [
        new EmbedBuilder()
          .setDescription(
            `Blowbot is the official Purdue Blows discord bot! To use one of Blowbot's commands, 
          just type /command_name, replacing command_name with your desired command! Currently, Blowbot supports 
          the following commands: 
          - add_song
          - get_random_song
          - get_song_info
          - get_song
          For more info on how to use each command, be sure to read the command descriptions!`
          )
          .setColor(getThemeColor("text")),
      ],
    });
  },
  cooldown: 1,
};

export default command;
