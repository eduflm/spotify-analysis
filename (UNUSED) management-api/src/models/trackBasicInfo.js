const mongoose = require('mongoose');

var TrackBasicInfoSchema = new mongoose.Schema({
  spotify_track_id: {
    type: String,
    required: true,
    unique: true
  },
  name: {
    type: String,
    required: true
  },
  artist: {
    type: String,
    required: true
  },
  track_link: {
    type: String,
    required: true
  },
  track_image: {
    type: String,
    required: true
  },
}, { timestamps: true })

var TrackBasicInfo = mongoose.model('TrackBasicInfo',TrackBasicInfoSchema);

module.exports = {TrackBasicInfo};