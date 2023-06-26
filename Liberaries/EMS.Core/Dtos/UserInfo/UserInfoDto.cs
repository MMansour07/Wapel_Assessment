using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.UserInfo
{
    public class UserInfoDto
    {
        public string Id { get; set; }
        [Required(ErrorMessage = "*")]
        public string FirstName { get; set; }
        [Required(ErrorMessage = "*")]
        public string LastName { get; set; }
        public string FullName { get { return FirstName + " " + LastName; } }
        [Required(ErrorMessage = "*")]
        public string CompanyName { get; set; }
        [Required(ErrorMessage = "*")]
        public string Phone { get; set; }
        [Required(ErrorMessage = "*")]
        [DataType(DataType.EmailAddress)]
        public string Email { get; set; }
        public int MediaCount { get; set; }
    }
}