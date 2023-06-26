using System;

namespace EMS.Core.Model
{
    public class Rating : BaseEntity
    {
        public float QualityScore { get; set; }
        public float EfficiencyScore { get; set; }
        public float TimelineScore { get; set; }
        public float AccuracyScore { get; set; }
        public string Remarks { get; set; }
        public string UserId { get; set; }
        public virtual User User { get; set; }
        public int TaskId { get; set; }
        public virtual Task Task { get; set; }

    }
}
