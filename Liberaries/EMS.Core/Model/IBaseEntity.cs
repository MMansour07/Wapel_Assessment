using System;

namespace EMS.Core.Model
{
    interface IBaseEntity
    {
        DateTime? CreatedDate { get; set; }
        DateTime? UpdatedDate { get; set; }
        bool IsActive { get; set; }
        bool IsDeleted { get; set; }
        string CreatedBy { get; set; }
        string UpdatedBy { get; set; }
    }
}
