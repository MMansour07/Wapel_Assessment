using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.Role
{
    public class CreateRoleDto
    {
        [Required(ErrorMessage ="*")]
        public string Name { get; set; }
    }
}