const mongoose = require('mongoose');

var ObjectId = mongoose.Schema.Types.ObjectId;

var ChartSchema = new mongoose.Schema({
  track_basic_info_id: {
    type: ObjectId,
    required: true,
    ref: 'TrackBasicInfo'
  },
  date: {
    type: Date
  },
  chart_position: {
    type: Number,
    required: true
  },
  number_of_streams: {
    type: Number,
    required: true
  },
  trend: {
    type: String,
    enum: ['up', 'down', 'neutral', 'new']
  },
}, { timestamps: true })

var Chart = mongoose.model('Chart',ChartSchema);

module.exports = {Chart};