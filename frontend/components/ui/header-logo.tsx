import Link from 'next/link'
import {TbPerfume} from "react-icons/tb"

export default function HeaderLogo() {
  return (
    <Link href="/" aria-label="Cruip" className="flex items-center">
      <TbPerfume size={40}/>
      <p className="ml-2 font-bold text-3xl">
        Skincare Hunt
      </p>
    </Link>
  )
}
