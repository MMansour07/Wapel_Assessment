

namespace EMS.Core.Dtos.User
{
    public class UserSelectListDto
    {
        public string Id { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string FullName { get { return FirstName + " " + LastName; } }
    }
}