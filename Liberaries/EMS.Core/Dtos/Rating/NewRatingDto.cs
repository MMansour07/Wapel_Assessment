using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.Rating
{
    public class NewRatingDto
    {
        [Required(ErrorMessage = "Required Field")]
        public float QualityScore { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public float EfficiencyScore { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public float TimelineScore { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public float AccuracyScore { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Remarks { get; set; }

        public string UserId { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public int TaskId { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public int TaskCriteriaId { get; set; }
    }
}