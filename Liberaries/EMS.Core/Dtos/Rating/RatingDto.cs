using EMS.Core.Dtos.Task;
using EMS.Core.Dtos.User;

namespace EMS.Core.Dtos.Rating
{
    public class RatingDto
    {
        public int Id { get; set; }
        public float QualityScore { get; set; }
        public float EfficiencyScore { get; set; }
        public float TimelineScore { get; set; }
        public float AccuracyScore { get; set; }
        public double TotalScore
        {
            get
            {
                return (this.QualityScore + this.EfficiencyScore + this.TimelineScore + this.AccuracyScore) / 3.0;
            }
        }
        public string Remarks { get; set; }
        public string UserId { get; set; }
        public int TaskId { get; set; }
        public string User { get; set; }
        public TaskDto Task { get; set; }
    }
}