using System;
using System.ComponentModel.DataAnnotations;

namespace EMS.Core.Dtos.UserInfo
{
    public class UpdateUserInfoDto
    {
        [Required(ErrorMessage = "*")]
        public string UserId { get; set; }
        public string Name { get; set; }
        public string LastName { get; set; }
        public string NationalCode { get; set; }
        public DateTime? BirthDate { get; set; }
        public string Details { get; set; }
        public string Image { get; set; }
        public byte[] ImageBytes { get; set; }
    }
}