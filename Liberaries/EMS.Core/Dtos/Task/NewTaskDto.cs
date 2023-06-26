


using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.Task
{
    public class NewTaskDto
    {
        [Required(ErrorMessage = "Required Field")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Details { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string SuccessIndicator { get; set; }

        public string ActualAccomplishment { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public int TaskCriteriaId { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string UserId { get; set; }
    }
}