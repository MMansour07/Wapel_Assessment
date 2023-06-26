using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.User
{
    public class RegisterUserDto
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
    }

    public class RegisterUserInfoDto
    {
        public string Name { get; set; }
        public string LastName { get; set; }
    }
}