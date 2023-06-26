using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.User
{
    public class SigninUserDto
    {
        //resourses file 
        [Required(ErrorMessage = "Required Field")]
        [DataType(DataType.EmailAddress)]
        [EmailAddress]
        public string Email { get; set;  }
        [Required(ErrorMessage = "Required Field")]
        public string Password { get; set; }
        public bool RememberMe { get; set; }
    }
}