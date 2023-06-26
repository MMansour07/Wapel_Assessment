using EMS.Core.Dtos.Role;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;

namespace EMS.Core.Dtos.User
{
    public class UserEditDto
    {
        public string Id { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string FirstName { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string LastName { get; set; }
        public string FullName { get { return FirstName + " " + LastName; } }

        [Required(ErrorMessage = "Required Field")]
        public string CompanyName { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Phone { get; set; }

        [Required(ErrorMessage = "Required Field")]
        [DataType(DataType.EmailAddress)]
        [EmailAddress]
        public string Email { get; set; }
        public string Username => (this.Email);

        [Required(ErrorMessage = "Required Field")]

        public List<string> SelectedRoles { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string DepartmentId { get; set; }
        public string ManagerId { get; set; }
    }
}