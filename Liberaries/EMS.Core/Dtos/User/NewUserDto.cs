using EMS.Core.Dtos.Role;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;

namespace EMS.Core.Dtos.User
{
    public class NewUserDto
    {
        [Required(ErrorMessage = "Required Field")]
        public string FirstName { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string LastName { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Phone { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string CompanyName { get; set; }

        [Required(ErrorMessage = "Required Field")]
        [DataType(DataType.EmailAddress)]
        public string Email { get; set; }

        public string Username => (this.Email);

        [Required(ErrorMessage = "Required Field")]
        [MinLength(6)]
        public string Password { get; set; }

        [Required(ErrorMessage = "Required Field")]
        [Compare("Password", ErrorMessage = "confirm pass does not match with the pass")]
        public string ConfirmPassword { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public List<string> SelectedRoles { get; set; }

        public List<GetRoleDto> Roles
        {
            get
            {
                return this.SelectedRoles.Select(x => new GetRoleDto() { RoleId = x }).ToList();
            }
        }

        [Required(ErrorMessage = "Required Field")]
        public string DepartmentId { get; set; }

        public string ManagerId { get; set; }

    }
}