using System.ComponentModel.DataAnnotations;


namespace EMS.Core.Dtos.TaskCriteria
{
    public class NewCriteriaDto
    {
        [Required(ErrorMessage = "Required Field")]
        public string Name { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Description { get; set; }
    }
}